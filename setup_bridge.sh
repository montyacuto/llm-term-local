#!/bin/bash
# setup_bridge.sh - Install dependencies for LLM Bridge Server

echo "Setting up LLM Bridge Server dependencies..."

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install Python and pip first."
    exit 1
fi

# Create a virtual environment (optional but recommended)
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install flask llama-cpp-python

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "Setup completed successfully!"
    echo ""
    echo "To run the LLM Bridge Server:"
    echo "1. Activate the virtual environment: source .venv/bin/activate"
    echo "2. Run the server: python llm_bridge_server.py --model-path /path/to/your/model.gguf"
    echo ""
    echo "For GPU acceleration:"
    echo "pip uninstall -y llama-cpp-python"
    echo "CMAKE_ARGS=\"-DLLAMA_CUBLAS=on\" pip install llama-cpp-python --no-cache-dir"
    echo ""
else
    echo "Setup failed. Please check the error messages above."
fi