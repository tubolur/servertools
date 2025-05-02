PYTHON_CMD="python3"
VENV_ACTIVATE_DIR="venv/bin/activate"

#creating venv & installing python libs
${PYTHON_CMD} -m venv venv
source ${VENV_ACTIVATE_DIR}
pip install -r utils/requirements.txt

