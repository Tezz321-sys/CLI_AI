import argparse
import sys
import json
from pathlib import Path
import os

class DummyFile:
    def write(self, x): pass
    def flush(self): pass
    def close(self): pass

dummy_file = DummyFile()

try:
    _old_stdout = sys.stdout
    sys.stdout = dummy_file
    import g4f
    g4f.debug.version_check = False
    g4f.debug.logging = False
    sys.stdout = _old_stdout
except ImportError:
    sys.stdout = _old_stdout
    print("Please install g4f package: pip install g4f")
    sys.exit(1)

CONFIG_DIR = Path.home() / ".chatgpt_cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

def init_config():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    init_config()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return [{"role": "system", "content": "You are a helpful assistant."}]

def save_history(history):
    init_config()
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)


def login():
    config = load_config()
    config['logged_in'] = True
    save_config(config)
    print("Logged in successfully. You are now using the free global proxy.")

def logout():
    config = load_config()
    if config.get('logged_in'):
        config['logged_in'] = False
        save_config(config)
        print("Logged out successfully.")
    else:
        print("Not logged in.")

def clear_history():
    if HISTORY_FILE.exists():
        os.remove(HISTORY_FILE)
    print("Conversation history cleared.")

def get_file_info(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return None
        
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
        return {"type": "image", "data": filepath}
    else:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"type": "text", "data": f"--- FILE: {os.path.basename(filepath)} ---\n{content}\n--- END FILE ---"}
        except Exception as e:
            print(f"Failed to read file as text: {e}")
            return None

def complete_chat(history, image_path=None):
    kwargs = {
        "model": g4f.models.default,
        "messages": history,
        "stream": True
    }
    
    if image_path:
        try:
            kwargs["image"] = open(image_path, "rb")
        except Exception as e:
            print(f"Failed to open image: {e}")
            return ""

    reply = ""
    _old_stdout = sys.stdout
    try:
        # Hide any internal initialization prints from g4f proxy loops
        sys.stdout = dummy_file
        response = g4f.ChatCompletion.create(**kwargs)
        sys.stdout = _old_stdout
        
        for chunk in response:
            if isinstance(chunk, str):
                try:
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                except UnicodeEncodeError:
                    sys.stdout.write(chunk.encode('ascii', 'ignore').decode('ascii'))
                    sys.stdout.flush()
                reply += chunk
        print() 
    except Exception as e:
        sys.stdout = _old_stdout
        print(f"\nError communicating with AI provider: {e}")
        
    return reply

def ask(prompt, file_arg=None):
    config = load_config()
    if not config.get('logged_in'):
        print("You are not logged in. Please run 'chatgpt login' first.")
        sys.exit(1)
    
    image_path = None
    if file_arg:
        file_info = get_file_info(file_arg)
        if hasattr(file_info, 'get') and file_info.get('type') == 'text':
            prompt += f"\n\n[Attached File Content]:\n{file_info['data']}"
        elif hasattr(file_info, 'get') and file_info.get('type') == 'image':
            image_path = file_info['data']
    
    history = load_history()
    history.append({"role": "user", "content": prompt})
    
    print("\nChatGPT: ", end="")
    reply = complete_chat(history, image_path)
    
    if reply:
        history.append({"role": "assistant", "content": reply})
        save_history(history)

def repl():
    config = load_config()
    if not config.get('logged_in'):
        print("You are not logged in. Please run 'chatgpt login' first.")
        sys.exit(1)
    
    print("Entering interactive mode.")
    print("Type 'quit' or 'exit' to leave.")
    print("To attach a file, type '/file <path-to-file>' (e.g. /file info.txt) and press Enter FIRST.")
    history = load_history()
    
    pending_file = None
        
    while True:
        try:
            prefix = ""
            if pending_file:
                prefix = f"[File: {os.path.basename(pending_file)}] "
            
            prompt = input(f"{prefix}You: ")
            
            if prompt.strip().lower() in ['quit', 'exit']:
                break
                
            if prompt.strip().startswith("/file "):
                filepath = prompt.strip()[6:].strip()
                if os.path.exists(filepath):
                    pending_file = filepath
                    print(f"File '{os.path.basename(filepath)}' attached! Now type your actual question.")
                else:
                    print(f"Error: File '{filepath}' not found.")
                continue
                
            if not prompt.strip():
                continue
            
            image_path = None
            if pending_file:
                file_info = get_file_info(pending_file)
                if file_info and file_info.get('type') == 'text':
                    prompt += f"\n\n[Attached File Content]:\n{file_info['data']}"
                elif file_info and file_info.get('type') == 'image':
                    image_path = file_info['data']
                pending_file = None
                
            history.append({"role": "user", "content": prompt})
            
            print("ChatGPT: ", end="")
            reply = complete_chat(history, image_path)
            
            if reply:
                history.append({"role": "assistant", "content": reply})
                save_history(history)
                
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="ChatGPT CLI - OS Independent (Free Version)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    subparsers.add_parser("login", help="Login to enable the AI assistance")
    subparsers.add_parser("logout", help="Logout and disable the AI assistance")
    
    ask_parser = subparsers.add_parser("ask", help="Ask a question (ex: chatgpt ask \"hello!\")")
    ask_parser.add_argument("prompt", nargs="+", type=str, help="The prompt to send to ChatGPT")
    ask_parser.add_argument("--file", "-f", type=str, help="Path to a text file or image to attach to your prompt", default=None)
    
    subparsers.add_parser("clear", help="Clear the conversation history")
    subparsers.add_parser("chat", help="Start an interactive chat session")
    
    args = parser.parse_args()
    
    if args.command == "login":
        login()
    elif args.command == "logout":
        logout()
    elif args.command == "ask":
        ask(" ".join(args.prompt), args.file)
    elif args.command == "clear":
        clear_history()
    elif args.command == "chat":
        repl()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
