# ChatGPT Free CLI

An OS-independent, completely free ChatGPT command-line interface. Uses global proxies via `g4f` to provide GPT chat directly in your terminal without requiring any API keys or subscriptions!

## Features
- **Zero Configuration**: Works completely free without any OpenAI API keys.
- **Cross-Platform**: Works identically on Windows, Linux, and macOS.
- **Persistent Sessions**: Log in once, and your history stays intact across terminal runs.
- **Interactive Chat**: Includes a live ChatGPT REPL environment with streaming responses.
- **File Uploads**: Supports injecting text file content and images into your conversation.

## Installation

You can clone this repository or download the source code, then run the handy installer for your specific operating system to make it available as a global bash tool.

### For Windows:
Double-click `install.bat` or run it from the command line:
```bat
.\install.bat
```

### For Linux / macOS:
Make the script executable and run it:
```bash
chmod +x install.sh
./install.sh
```

## How to Use

1. **Activate the system** *(You only need to do this once)*
   ```bash
   chatgpt login
   ```
2. **Start a continuous chat**
   ```bash
   chatgpt chat
   ```
3. **Ask a quick single question**
   ```bash
   chatgpt ask "Tell me a joke"
   ```
4. **Attach a file**
   ```bash
   chatgpt ask "Please summarize this document" -f document.txt
   ```
   *(Or type `/file path/to/document.txt` while inside the interactive chat mode).*
