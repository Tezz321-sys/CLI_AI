# Troubleshooting & Debugging Guide

Here are the most common issues you might run into while installing or running the ChatGPT CLI on different operating systems, and exactly how to fix them!

## Issue 1: "The process cannot access the file because it is being used" (Windows)
**Error:** `[WinError 32]` or `Permission Denied` during installation.
**Cause:** You are trying to run the installer while the `chatgpt chat` window is actively open in another terminal. Windows locks the executable while it is running.
**Fix:** Type `quit` or close your currently open ChatGPT terminal, then try running `install.bat` again.

## Issue 2: "externally-managed-environment" (Kali Linux / Debian)
**Error:** `PEP 668` error when locally running the installer script on Linux. 
**Cause:** Modern Linux distributions strictly prevent global `pip` installations to protect native system files.
**Fix:** Run the manual installation commands in your terminal and append the system bypass override flag:
```bash
pip install -r requirements.txt --break-system-packages
pip install -e . --break-system-packages
```

## Issue 3: The terminal freezes and hangs indefinitely (Linux)
**Cause:** The background `g4f` scraping proxy is missing advanced web components needed to spoof Cloudflare and anti-bot checks on strict Linux environments.
**Fix:** Stop the freeze by hitting `CTRL+C`, and install the advanced networking bundles:
```bash
sudo pip install -U g4f[all] curl_cffi --break-system-packages
```

## Issue 4: Emoji or Unicode Encoding Crash (Windows CMD)
**Error:** `'charmap' codec can't encode character...`
**Cause:** The AI generated a complex emoji or foreign symbol, but you are using an older Windows Command Prompt that does not natively stream UTF-8 sequences.
**Fix:** The application attempts to safely ignore and strip unreadable emojis. However, for full visual support, you can enable modern Unicode mode by running `chcp 65001` in your terminal before chatting!
