#!/bin/sh

# Get the path to the virtual environment activation script
VENV_PATH=$(grep "^INSTALL_PYTHON='" ./.git/hooks/pre-commit | sed "s/INSTALL_PYTHON='//" | sed "s/python.*//" | tr \\ /)
VENV_ACTIVATION_SCRIPT="${VENV_PATH}activate"

# Insert the virtual environment activation line at line 5
sed -i "5i source \"$VENV_ACTIVATION_SCRIPT\"" ./.git/hooks/pre-commit
echo "Pre-commit configuration added to the file with virtual environment activation."
