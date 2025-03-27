#!/bin/bash

# Check if conda command is available
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed or not in your PATH. Please install Conda first."
    exit 1
fi

# Source conda shell integration (adjust the path if necessary)
source "$(conda info --base)/etc/profile.d/conda.sh"

# Get current directory name
CURRENT_DIR=$(basename "$(pwd)")

# Check if environment.yml exists
if [ -f environment.yml ]; then
    echo "Creating Conda environment from environment.yml in current directory..."
    # Create environment in the current directory
    conda env create -f environment.yml --prefix ./env
    ENV_PATH="./env"
else
    echo "environment.yml not found. Creating default environment in current directory..."
    ENV_PATH="./env"
    conda create --prefix "$ENV_PATH" python=3.9 -y
fi

# Activate the local environment
conda activate "$ENV_PATH"

# Create a .envrc file for direnv (if installed)
echo "export CONDA_PREFIX=\"$(pwd)/env\"" > .envrc
echo "conda activate \"$(pwd)/env\"" >> .envrc

echo "Conda environment created at '$ENV_PATH' and activated!"
echo "Note: To reactivate this environment later, use: conda activate $ENV_PATH"

