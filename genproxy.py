#!/usr/bin/env python3
"""
Proxy Generator and Checker with Telegram Bot
"""

import requests
import time
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Your Telegram Bot Token
TELEGRAM_TOKEN = "8534562300:AAEXY5j-i8cPmsw1E_YiW-OGSRar7LscSSk"

# Proxy sources
PROXY_API = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all"
USA_PROXY_API = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=US"

TEST_URL = "http://httpbin.org/ip"
TEST_TIMEOUT = 5

# Store proxies
live_proxies = []
dead_proxies = []


def fetch_proxies(country="all"):
    """Fetch proxies from API"""
    proxies = []
    try:
        if country.upper() == "USA":
            api_url = USA_PROXY_API
        else:
            api_url = PROXY_API
        
        print(f"Fetching proxies from: {api_url}")
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            proxies = response.text.strip().split('\n')
            proxies = [p.strip() for p in proxies if p.strip()]
            print(f"Got {len(proxies)} proxies")
    except Exception as e:
        print(f"Error fetching: {e}")
    
    return proxies


def check_proxy(proxy):
    """Check if proxy is working"""
    try:
        resp = requests.get(TEST_URL, proxies={"http": proxy, "https": proxy}, timeout=TEST_TIMEOUT)
        return resp.status_code == 200
    except:
        return False


def check_proxies(proxy_list, max_check=10):
    """Check all proxies"""
    global live_proxies, dead_proxies
    live_proxies = []
    dead_proxies = []
    
    to_check = proxy_list[:max_check]
    total = len(to_check)
    
    print(f"Checking {total} proxies...")
    
    for i, proxy in enumerate(to_check, 1):
        print(f"[{i}/{total}] {proxy}", end=" ")
        
        if check_proxy(proxy):
            print("LIVE")
            live_proxies.append(proxy)
        else:
            print("DEAD")
            dead_proxies.append(proxy)
        
        time.sleep(0.3)
    
    return live_proxies, dead_proxies


def run_check(country="all", max_check=10):
    """Run proxy check"""
    print(f"\n=== STARTING PROXY CHECK ({country}) ===")
    print(f"Time: {datetime.now()}")
    
    proxies = fetch_proxies(country)
    
    if not proxies:
        return [], []
    
    return check_proxies(proxies, max_check)


# Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    await update.message.reply_text(
        "Proxy Generator Bot\n\n"
        "Commands:\n"
        "/gen - Generate & check all proxies\n"
        "/usa - Generate & check USA proxies\n"
        "/list - Show live proxies"
    )


async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gen command"""
    chat_id = update.effective_chat.id
    
    # Send processing message
    msg = await context.bot.send_message(chat_id, "Checking proxies... Please wait...")
    
    try:
        live, dead = run_check("all", max_check=10)
        
        # Build response
        response = f"CHECK COMPLETE\n"
        response += f"=============\n\n"
        
        if live:
            response += f"LIVE PROXIES ({len(live)}):\n"
            for p in live:
                ip, port = p.split(":") if ":" in p else (p, "")
                response += f"IP: {ip}\nPort: {port}\nUser: (none)\nPass: (none)\n\n"
        else:
            response += "No live proxies found.\n\n"
        
        if dead:
            response += f"DEAD PROXIES ({len(dead)}):\n"
            for p in dead:
                response += f"{p}\n"
        
        # Send response
        await context.bot.edit_message_text(response, chat_id, msg.message_id)
        
    except Exception as e:
        await context.bot.edit_message_text(f"Error: {str(e)}", chat_id, msg.message_id)


async def usa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """USA command"""
    chat_id = update.effective_chat.id
    
    msg = await context.bot.send_message(chat_id, "Checking USA proxies... Please wait...")
    
    try:
        live, dead = run_check("USA", max_check=10)
        
        response = f"USA PROXY CHECK COMPLETE\n"
        response += f"=======================\n\n"
        
        if live:
            response += f"LIVE PROXIES ({len(live)}):\n"
            for p in live:
                ip, port = p.split(":") if ":" in p else (p, "")
                response += f"IP: {ip}\nPort: {port}\nUser: (none)\nPass: (none)\n\n"
        else:
            response += "No live USA proxies found.\n\n"
        
        if dead:
            response += f"DEAD PROXIES ({len(dead)}):\n"
            for p in dead:
                response += f"{p}\n"
        
        await context.bot.edit_message_text(response, chat_id, msg.message_id)
        
    except Exception as e:
        await context.bot.edit_message_text(f"Error: {str(e)}", chat_id, msg.message_id)


async def list_proxies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List command"""
    if live_proxies:
        response = "LIVE PROXIES:\n\n"
        for p in live_proxies:
            ip, port = p.split(":") if ":" in p else (p, "")
            response += f"IP: {ip}\nPort: {port}\n\n"
    else:
        response = "No live proxies. Use /gen first."
    
    await update.message.reply_text(response)


def main():
    """Main function"""
    print("=" * 50)
    print("PROXY BOT STARTING")
    print("=" * 50)
    print(f"Token: {TELEGRAM_TOKEN}")
    print("=" * 50)
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen))
    app.add_handler(CommandHandler("usa", usa))
    app.add_handler(CommandHandler("list", list_proxies))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: u.message.reply_text("Use /gen or /usa")))
    
    print("Bot running! Send /gen or /usa")
    app.run_polling()


if __name__ == "__main__":
    main()
