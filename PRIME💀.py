import os
import sys
import json
import asyncio
import random
import threading
import time
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
import requests

CONFIG_FILE = ".speedx_config.json"
VIP_PASSWORD = "speedxvip"
SESSION_NAME = "speedx_session"

# Terminal Colors
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

# ✅ Fixed ASCII Art
def print_credit():
    ascii_art = f"""
{RED}██████   ██   ██  ██████   ███████ ████████     ██   ██ 
 ██    ██  ██   ██ ██    ██ ██         ██        ██   ██ 
 ██    ██  ███████ ██    ██ ███████    ██        ███████ 
 ██    ██  ██   ██ ██    ██      ██    ██        ██   ██ 
  ██████   ██   ██  ██████  ███████    ██        ██   ██ 
                                                       
██   ██ 
██   ██ 
██   ██ 
██   ██ 
 █████
{YELLOW}           🔥 C R E A T E D   B Y   S P E E D _ X 🔥{RESET}
    """
    print(ascii_art)

# Rainbow loading spinner
def flashy_loading():
    spinner = ['|', '/', '-', '\\']
    print(f"{CYAN}Initializing SPEED_X VIP SYSTEM...{RESET}")
    for i in range(50):
        sys.stdout.write(f"\r{MAGENTA}LOADING {spinner[i % 4]} {i*2}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.03)
    print(f"\r{GREEN}LOADING COMPLETE!{RESET}\n")

# Load config or prompt
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        print("🔐 First time setup - Enter your API Info:\n")
        api_id = int(input("📲 api_id: "))
        api_hash = input("🔐 api_hash: ")
        config = {"api_id": api_id, "api_hash": api_hash}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return config

# Bot Spammer
def bot_spam(token, chat_id, message, limit):
    for i in range(limit):
        try:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={
                "chat_id": chat_id,
                "text": message
            })
            print(f"{GREEN}[BOT] ✅ Sent #{i+1}: {message}{RESET}")
            time.sleep(0.3)
        except Exception as e:
            print(f"{RED}[BOT] ❌ Error: {e}{RESET}")
            break

# Main async USER SPAM
async def user_spam(api_id, api_hash):
    phone = input("📞 Your Phone Number (Start with 880): ")
    client = TelegramClient(SESSION_NAME, api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input("📩 Enter the code you received: ")
        await client.sign_in(phone, code)

    print(f"{GREEN}✅ Telegram Login Success!{RESET}")
    target = input("🎯 Target Username (without @): ")
    msg = input("💬 Message to send: ")
    limit = 20
    delay = 0.2

    vip = input("👑 Enable VIP Mode? (yes/no): ").strip().lower()
    if vip == "yes":
        pw = input("🔐 Enter VIP password: ")
        if pw == VIP_PASSWORD:
            print(f"{CYAN}✅ VIP Unlocked: MAX SPEED!{RESET}")
            limit = 99999
            delay = 0.05
        else:
            print(f"{RED}❌ Wrong Password. Continuing with normal speed.{RESET}")

    print(f"{YELLOW}🚀 Starting spam to @{target} ...{RESET}")
    for i in range(limit):
        try:
            await client.send_message(target, msg)
            print(f"{GREEN}✅ Sent #{i+1}: {msg}{RESET}")
            await asyncio.sleep(delay)
        except FloodWaitError as e:
            print(f"{RED}⏳ FloodWait: Sleeping for {e.seconds}s{RESET}")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"{RED}❌ Error: {e}{RESET}")
            break
    await client.disconnect()
    print(f"{CYAN}👋 Spam complete. Stay SPEED_X.{RESET}")

# Main Runner
def run():
    os.system("cls" if os.name == "nt" else "clear")
    print_credit()
    flashy_loading()
    config = load_config()

    print(f"\n{YELLOW}Select Spam Mode:{RESET}")
    print("1. USER SPAM (Login with phone)")
    print("2. BOT SPAM (Use bot token)")
    choice = input("🔘 Your Choice (1/2): ")

    if choice == "1":
        asyncio.run(user_spam(config["api_id"], config["api_hash"]))
    elif choice == "2":
        token = input("🤖 Bot Token: ")
        chat_id = input("💬 Chat ID or @username: ")
        message = input("📨 Message to send: ")
        try:
            limit = int(input("🔁 How many times?: "))
        except:
            limit = 20
        bot_spam(token, chat_id, message, limit)
    else:
        print(f"{RED}❌ Invalid option. Exiting...{RESET}")

# Run main
if __name__ == "__main__":
    run()