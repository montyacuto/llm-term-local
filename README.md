# 🖥️ LLM-Term

A Rust-based CLI tool that generates and executes terminal commands using OpenAI's language models, local Ollama models, or llama-cpp-python with .gguf models.

## Features

- Configurable model and token limit (gpt-4o-mini, gpt-4o, Ollama, or llama-cpp-python with .gguf models)
- Generate and execute terminal commands based on user prompts
- Works on both PowerShell and Unix-like shells (Automatically detected)
- Caching of commands for repeated use
- Support for local inference with Ollama or llama-cpp-python

## Demo

![LLM-Term Demo](vhs-video/demo.gif)

## Installation

- Download the binary from the [Releases](https://github.com/dh1011/llm-term/releases) page

- Set PATH to the binary

    - MacOS/Linux:
    ```
    export PATH="$PATH:/path/to/llm-term"
    ```
    - To set it permanently, add `export PATH="$PATH:/path/to/llm-term"` to your shell configuration file (e.g., `.bashrc`, `.zshrc`)

    - Windows:
    ```
    set PATH="%PATH%;C:\path\to\llm-term"
    ```
    - To set it permanently, add `set PATH="%PATH%;C:\path\to\llm-term"` to your shell configuration file (e.g., `$PROFILE`)

## Development

1. Clone the repository
2. Build the project using Cargo: `cargo build --release`
3. The executable will be available in the `target/release` directory

## Usage

1. Set your OpenAI API key (if using OpenAI models):

   - MacOS/Linux:
     ```
     export OPENAI_API_KEY="sk-..."
     ```

   - Windows:
     ```
     set OPENAI_API_KEY="sk-..."
     ```

2. If using Ollama, make sure it's running locally on the default port (11434)

3. If using llama-cpp-python, set up the bridge server (see instructions below)

4. Run the application with a prompt:

   ```
   ./llm-term "your prompt here"
   ```

5. The app will generate a command based on your prompt and ask for confirmation before execution.

## Using llama-cpp-python with .gguf models

### Setup

1. Install Python dependencies:
   ```
   chmod +x setup_bridge.sh
   ./setup_bridge.sh
   ```

2. Start the bridge server with your .gguf model:
   ```
   chmod +x start_bridge.sh
   ./start_bridge.sh /path/to/your/model.gguf
   ```
   
   Optional arguments:
   ```
   ./start_bridge.sh <model_path> [port] [host] [context_size] [gpu_layers]
   ```

3. Configure LLM-Term to use llama-cpp-python:
   ```
   ./llm-term --config
   ```
   
   Select option 4 and provide the path to your .gguf model and the bridge server URL.

### GPU Acceleration

For GPU acceleration with CUDA:

```bash
pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --no-cache-dir
```

For GPU acceleration with Metal (MacOS):

```bash
pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --no-cache-dir
```

## Configuration

A `config.json` file will be created in the same directory as the binary on first run. You can modify this file to change the default model and token limit.

## Options

- `-c, --config`: Run configuration setup or specify a custom config file path
- `--disable-cache`: Disable command caching and always query the LLM

## Supported Models

- OpenAI GPT-4 (gpt-4o)
- OpenAI GPT-4 Mini (gpt-4o-mini)
- Ollama (local models, default: llama3.1)
- llama-cpp-python (with .gguf model files)