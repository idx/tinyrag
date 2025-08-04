#!/usr/bin/env python3
"""
Test streaming functionality to debug the issue
"""
import gradio as gr
from llm import get_llm_stream

def simple_stream_test(message, history):
    """Simple streaming test without RAG"""
    messages = []
    
    # Convert Gradio history format to OpenAI format
    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    # Stream the response
    response_text = ""
    for chunk in get_llm_stream(messages):
        response_text += chunk
        yield response_text

# Create simple ChatInterface for testing
demo = gr.ChatInterface(
    simple_stream_test,
    title="Streaming Test",
    description="Testing LLM streaming without RAG"
)

if __name__ == "__main__":
    demo.launch()