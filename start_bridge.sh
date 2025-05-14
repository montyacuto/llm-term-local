#!/bin/bash
# start_bridge.sh - Start the LLM Bridge Server

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <model_path> [port] [host] [n_ctx] [n_gpu_layers]"
    echo "Example: $0 ./models/llama-2-7b-chat.gguf 8000 127.0.0.1 2048 0"
    exit 1
fi

MODEL_PATH="$1"
PORT="${2:-8000}"
HOST="${3:-127.0.0.1}"
N_CTX="${4:-2048}"
N_GPU_LAYERS="${5:-0}"

# Check if the model file exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: Model file '$MODEL_PATH' does not exist."
    exit 1
fi

# Check if virtual environment exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Warning: No virtual environment found at '.venv'."
    echo "Running with system Python. Dependencies might be missing."
fi

# Check if llm_bridge_server.py exists
if [ ! -f "llm_bridge_server.py" ]; then
    echo "Error: llm_bridge_server.py not found in the current directory."
    exit 1
fi

echo "Starting LLM Bridge Server..."
echo "Model path: $MODEL_PATH"
echo "Server: $HOST:$PORT"
echo "Context size: $N_CTX"
echo "GPU layers: $N_GPU_LAYERS"
echo ""

# Start the server
python llm_bridge_server.py \
    --model-path "$MODEL_PATH" \
    --port "$PORT" \
    --host "$HOST" \
    --n-ctx "$N_CTX" \
    --n-gpu-layers "$N_GPU_LAYERS"