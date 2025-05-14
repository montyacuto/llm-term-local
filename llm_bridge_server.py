#!/usr/bin/env python3
"""
LLM Bridge Server for LLM-Term
Provides an OpenAI-compatible API for llama-cpp-python models
"""

import argparse
import json
import logging
import os
from typing import Dict, List, Optional, Union

from flask import Flask, jsonify, request
from llama_cpp import Llama

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("llm-bridge")

app = Flask(__name__)

# Global model instance
model = None


def load_model(
    model_path: str,
    n_ctx: int = 2048,
    n_threads: Optional[int] = None,
    n_gpu_layers: int = 0,
    verbose: bool = False,
) -> Llama:
    """Load a .gguf model using llama-cpp-python."""
    logger.info(f"Loading model from {model_path}")
    
    # If n_threads is not provided, use all available cores
    if n_threads is None:
        import multiprocessing
        n_threads = multiprocessing.cpu_count()
    
    return Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_gpu_layers=n_gpu_layers,
        verbose=verbose,
    )


def format_openai_response(
    model_name: str, 
    prompt: str, 
    response: str, 
    tokens_used: int
) -> Dict:
    """Format response like OpenAI API."""
    return {
        "id": "cmpl-temp-id",
        "object": "chat.completion",
        "created": int(__import__("time").time()),
        "model": model_name,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response.strip()
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": tokens_used // 2,  # Estimate
            "completion_tokens": tokens_used // 2,  # Estimate
            "total_tokens": tokens_used
        }
    }


@app.route("/v1/chat/completions", methods=["POST"])
def chat_completion():
    """Handle chat completion requests."""
    global model
    
    try:
        data = request.json
        
        # Extract parameters
        messages = data.get("messages", [])
        max_tokens = data.get("max_tokens", 256)
        temperature = data.get("temperature", 0.7)
        
        # Build prompt from messages
        prompt = ""
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "system":
                prompt += f"[SYSTEM]: {content}\n\n"
            elif role == "user":
                prompt += f"[USER]: {content}\n\n"
            elif role == "assistant":
                prompt += f"[ASSISTANT]: {content}\n\n"
                
        prompt += "[ASSISTANT]: "
        
        logger.info(f"Generating completion with {len(prompt)} chars prompt")
        
        # Generate completion
        response = model.create_completion(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["[USER]:", "[SYSTEM]:"],
        )
        
        # Format and return response
        completion_text = response["choices"][0]["text"]
        tokens_used = response["usage"]["total_tokens"]
        model_name = os.path.basename(args.model_path)
        
        return jsonify(format_openai_response(
            model_name=model_name,
            prompt=prompt,
            response=completion_text,
            tokens_used=tokens_used
        ))
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Bridge Server for LLM-Term")
    parser.add_argument("--model-path", type=str, required=True, help="Path to .gguf model file")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on")
    parser.add_argument("--n-ctx", type=int, default=2048, help="Context window size")
    parser.add_argument("--n-threads", type=int, help="Number of threads to use (default: all cores)")
    parser.add_argument("--n-gpu-layers", type=int, default=0, help="Number of layers to offload to GPU")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Load the model
    model = load_model(
        model_path=args.model_path,
        n_ctx=args.n_ctx,
        n_threads=args.n_threads,
        n_gpu_layers=args.n_gpu_layers,
        verbose=args.verbose,
    )
    
    logger.info(f"Starting server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)