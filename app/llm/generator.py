# app/llm/generator.py

import os
import requests
import openai
from app.core.config import USE_LOCAL_LLM, LLM_PROVIDER, OPENAI_API_KEY, CLAUDE_API_KEY, OLLAMA_URL

def generate_answer(context: str, query: str) -> str:
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.
    
Context:
{context}

Question: {query}
Answer:"""

    if USE_LOCAL_LLM and LLM_PROVIDER == "ollama":
        return _call_ollama(prompt)
    elif LLM_PROVIDER == "openai":
        return _call_openai(prompt)
    elif LLM_PROVIDER == "anthropic":
        return _call_claude(prompt)
    else:
        return "[ERROR] No valid LLM backend selected."

def _call_openai(prompt: str) -> str:
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-4
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message['content']

def _call_claude(prompt: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    json = {
        "model": "claude-3-opus-20240229",  # or haiku/sonnet
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=json)
    return response.json()["content"][0]["text"]

def _call_ollama(prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "[No output from Ollama]")
