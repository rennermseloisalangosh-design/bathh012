@echo off
cd /d "c:\genrate proxy"
echo Starting Proxy Bot...
:start
python genproxy.py
echo Bot stopped, restarting in 5 seconds...
timeout /t 5 /nobreak
goto start
