# app/core/config.py

import os
from dotenv import load_dotenv

# Load .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docker', '.env')
load_dotenv(env_path)

USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "False").lower() == "true"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, ollama

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# import os
# from dotenv import load_dotenv

# # Load .env file
# env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docker', '.env')
# load_dotenv(env_path)

# USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "False").lower() == "false"
# LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, ollama

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
# OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")