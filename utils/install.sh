TARGET_USER="public"
PYTHON_CMD="python"
INSTALL_NAME="servertools"
INSTALL_DIR="/usr/share/dev/${INSTALL_NAME}"
USER_INSTALL_DIR="/home/${TARGET_USER}/dev/servertools/utils"
VENV_ACTIVATE_DIR="venv/bin/activate"

currentDir="(pwd)"
parentDir="$(dirname "$dir")"

#creating venv & installing python libs
${PYTHON_CMD} -m venv venv
source ${VENV_ACTIVATE_DIR}
pip install -r utils/requirements.txt

#making source ref dir
sudo mkdir -p "${INSTALL_DIR}"
sudo cp -R "$currentDir"/* "${INSTALL_DIR}"

#making user dir
mkdir -p "${USER_INSTALL_DIR}"

#adding command to bash_aliases or bashrc file
aliasesFile="/home/${TARGET_USER}/.bash_aliases"
bashrcFile="/home/${TARGET_USER}/.bashrc"
if [ ! -e "$aliasesFile" ]; then
    destFile=$bashrcFile
else 
    destFile=$aliasesFile
fi 
commandS="source ${INSTALL_DIR}/${VENV_ACTIVATE_DIR} && ${PYTHON_CMD} ${INSTALL_DIR}/runHTTPS.py"
commandMB="source ${INSTALL_DIR}/${VENV_ACTIVATE_DIR} && ${PYTHON_CMD} ${INSTALL_DIR}/runMessageBoard.py"
echo "alias httpsserver='${commandS}'" >> "$destFile"
echo "alias messageboard='${commandMB}'" >> "$destFile"
