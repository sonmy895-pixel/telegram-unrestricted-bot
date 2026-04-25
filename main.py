import io
import json
import logging
import os
import sqlite3
import sys
from pathlib import Path

import telebot
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("telegram-ai-bot")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENROUTER_BASE_URL = os.environ.get("AI_INTEGRATIONS_OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_API_KEY = os.environ.get("AI_INTEGRATIONS_OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    log.error("TELEGRAM_BOT_TOKEN is not set.")
    sys.exit(1)
if not OPENROUTER_BASE_URL or not OPENROUTER_API_KEY:
    log.error("OpenRouter env vars are missing. Set OPENROUTER_API_KEY.")
    sys.exit(1)

MODEL = "meta-llama/llama-3.3-70b-instruct:free"
SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant chatting with users on Telegram. "
    "Keep replies concise and easy to read on a phone. Use plain text and short "
    "paragraphs.\n\n"
    "You can call the `web_search` tool when the user asks about real-time, "
    "recent, or factual information you may not know. Cite sources by URL when "
    "you use it.\n\n"
    "Users can attach PDF or TXT files. The extracted file text is added to the "
    "conversation as a user message prefixed with `[Attached file: <name>]`. "
    "Use that text to answer follow-up questions about the file.\n\n"
    "If a request is unsafe or against policy, politely decline and offer a safer "
    "alternative."
)
MAX_HISTORY_TURNS = 12
MAX_REPLY_CHARS = 4000
MAX_FILE_CHARS = 30000
MAX_TOOL_ITERATIONS = 4
SEARCH_RESULT_COUNT = 5

# Data directory handling
DB_PATH = Path("bot.db")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client =
