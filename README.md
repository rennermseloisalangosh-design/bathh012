# Proxy Generator Telegram Bot

A Telegram bot that auto-generates proxy IPs, checks if they're live, and shows results.

## Deploy to Render (Free)

1. **Push code to GitHub**
   - Create a GitHub repository
   - Upload these files: genproxy.py, requirements.txt, Procfile, runtime.txt

2. **Deploy to Render**
   - Go to https://render.com and sign up
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - Build Command: (leave empty)
     - Start Command: python genproxy.py
   - Click "Deploy"

3. **Wait 2-3 minutes** for deployment to complete

4. **Open Telegram** and use your bot!

## Bot Commands
- `/gen` - Check all proxies
- `/usa` - Check USA proxies
- `/list` - Show live proxies

## Local Run
```
python genproxy.py
```

Or use the batch file:
```
run_bot.bat
