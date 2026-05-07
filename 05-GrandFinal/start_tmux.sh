#!/bin/bash

set -euo pipefail

session="my-project"

# Resolve important paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_ACTIVATE="${PROJECT_ROOT}/.venv/bin/activate"
PX4_DIR="${HOME}/PX4-Autopilot"
QGC_APP="${HOME}/Apps/QGround-5.0.8.AppImage"
MISSION_SCRIPT="${SCRIPT_DIR}/offboard_position_velocity_ned.py"

echo "Using project root: ${PROJECT_ROOT}"
echo "Session name: ${session}"

# Basic path validation for this project
if [ ! -d "${PROJECT_ROOT}" ]; then
	echo "[ERROR] Project root not found: ${PROJECT_ROOT}" >&2
	exit 1
fi

if [ ! -f "${MISSION_SCRIPT}" ]; then
	echo "[ERROR] Mission script not found: ${MISSION_SCRIPT}" >&2
	exit 1
fi

if [ ! -f "${VENV_ACTIVATE}" ]; then
	echo "[WARNING] Python venv not found at ${VENV_ACTIVATE}. Mission will run without venv." >&2
fi

if [ ! -d "${PX4_DIR}" ]; then
	echo "[WARNING] PX4 directory not found at ${PX4_DIR}. First window command may fail." >&2
fi

if [ ! -f "${QGC_APP}" ]; then
	echo "[WARNING] QGroundControl not found at ${QGC_APP}. Second window command may fail." >&2
fi

# If the session already exists, just attach to it
if tmux has-session -t "${session}" 2>/dev/null; then
	echo "tmux session '${session}' already exists. Attaching..."
	exec tmux attach -t "${session}"
fi

echo "Starting new tmux session '${session}'..."

# Window 1: PX4 SITL with gz_x500_mono_cam
tmux new-session -d -s "${session}" -n "PX4-SITL" \
	"cd \"${PX4_DIR}\" && make px4_sitl gz_x500_mono_cam"

# Window 2: QGroundControl
tmux new-window -t "${session}:" -n "QGroundControl" \
	"\"${QGC_APP}\""

# Window 3: Mission (Python offboard script in this project)
if [ -f "${VENV_ACTIVATE}" ]; then
	tmux new-window -t "${session}:" -n "Mission" \
		"cd \"${SCRIPT_DIR}\" && source \"${VENV_ACTIVATE}\" && python offboard_position_velocity_ned.py"
else
	tmux new-window -t "${session}:" -n "Mission" \
		"cd \"${SCRIPT_DIR}\" && python offboard_position_velocity_ned.py"
fi

echo "tmux session '${session}' is ready. Attaching..."
exec tmux attach -t "${session}"

