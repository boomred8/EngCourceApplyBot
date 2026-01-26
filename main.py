import  os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

telegram_user_id = os.getenv("USER_ID")

ai_token = os.getenv("OPENAI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")
HF_API_URL = os.getenv("HF_API_URL")


if not bot_token:
    raise ValueError("BOT_TOKEN environment variable not set")

