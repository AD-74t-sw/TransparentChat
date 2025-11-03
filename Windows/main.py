from google import genai

import threading
import pyperclip
import keyboard
import dotenv
import json
import time
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

dotenv.load_dotenv()

PROMPT_PATH = os.environ.get("PROMPT_PATH") + os.environ.get("PROMPT_NAME")
PROMPT_BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompt_base.json")
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")
TXT_HOTKEY_COMBINATION = os.environ.get("TXT_HOTKEY_COMBINATION", "ctrl+shift+o")
DIRECT_HOTKEY_COMBINATION = os.environ.get("DIRECT_HOTKEY_COMBINATION", "ctrl+shift+d+")
DEBUG = os.environ.get("DEBUG", "false").lower() in ("true", "1", "yes")
VERBOSE = os.environ.get("VERBOSE", "true").lower() in ("true", "1", "yes")

client = genai.Client(api_key=API_KEY)

def debug_print(message: str):
    if DEBUG and VERBOSE:
        print(message)

def verbose_print(message: str):
    if VERBOSE:
        print(message)

def load_prompt_base() -> dict:
    try:
        with open(PROMPT_BASE_PATH, "r", encoding="utf-8") as f:
            prompts = json.load(f)
        return {p["id"]: p["content"] for p in prompts}
    except Exception as e:
        debug_print(f"[DEBUG] ERROR loading prompt_base.json: {e}")
        return {}

def build_full_prompt(file_content: str, prompt_bases: dict) -> str:
    lines = file_content.strip().split('\n')
    
    if not lines:
        raise ValueError("File is empty")
    
    try:
        prompt_id = int((lines[0].strip())[0])
    except ValueError:
        raise ValueError(f"First line must be a number (prompt base ID), found: {lines[0]}")
    
    if prompt_id not in prompt_bases:
        raise ValueError(f"Prompt base with ID {prompt_id} not found")
    
    base_content = prompt_bases[prompt_id]

    user_content = '\n'.join(lines[1:]).strip()

    full_prompt = base_content + user_content
    
    return full_prompt

def build_direct_prompt(clipboard_content: str, prompt_id: int, prompt_bases: dict) -> str:
    if prompt_id not in prompt_bases:
        raise ValueError(f"Prompt base with ID {prompt_id} not found")
    
    base_content = prompt_bases[prompt_id]
    full_prompt = base_content + clipboard_content.strip()
    
    return full_prompt

def call_gemini(prompt_text: str) -> str:
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not defined in environment.")
    
    debug_print("[DEBUG] Sending prompt to Gemini...")
    debug_print(f"[DEBUG] Prompt (first 200 chars): {prompt_text[:500]}...")
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_text
        )
        result = response.text.strip()
        
        debug_print("[DEBUG] Response received from Gemini.")
        debug_print(f"[DEBUG] Response (first 100 chars): {result[:100]}...")
        
        return result
    except Exception as e:
        raise RuntimeError(f"Error generating Gemini response: {e}")

def handle_action():
    try:
        debug_print(f"\n[DEBUG] Hotkey {TXT_HOTKEY_COMBINATION.upper()} detected!")
        
        prompt_bases = load_prompt_base()
        if not prompt_bases:
            debug_print("[DEBUG] ERROR: Could not load base prompts")
            return
        
        debug_print(f"[DEBUG] Base prompts loaded: {list(prompt_bases.keys())}")
        
        if not os.path.exists(PROMPT_PATH):
            debug_print(f"[DEBUG] ERROR: File not found {PROMPT_PATH}")
            return
        
        debug_print(f"[DEBUG] Reading file from: {PROMPT_PATH}")
        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            file_content = f.read()
        
        if not file_content.strip():
            debug_print("[DEBUG] ERROR: File is empty")
            return
        
        debug_print(f"[DEBUG] File read successfully ({len(file_content)} characters)")
        
        full_prompt = build_full_prompt(file_content, prompt_bases)
        debug_print(f"[DEBUG] Full prompt built ({len(full_prompt)} characters)")
        
        result = call_gemini(full_prompt)
        
        pyperclip.copy(result)
        verbose_print("✓ Response copied to clipboard")
        
    except Exception as e:
        debug_print(f"[DEBUG] ERROR: {type(e).__name__}: {str(e)}")
        verbose_print(f"✗ Error: {str(e)}")

def handle_direct_action(prompt_id: int):
    try:
        debug_print(f"\n[DEBUG] Direct hotkey detected for prompt ID {prompt_id}!")
        
        prompt_bases = load_prompt_base()
        if not prompt_bases:
            debug_print("[DEBUG] ERROR: Could not load base prompts")
            return
        
        clipboard_content = pyperclip.paste()
        
        if not clipboard_content.strip():
            debug_print("[DEBUG] ERROR: Clipboard is empty")
            return
        
        debug_print(f"[DEBUG] Clipboard content read ({len(clipboard_content)} characters)")
        
        full_prompt = build_direct_prompt(clipboard_content, prompt_id, prompt_bases)
        debug_print(f"[DEBUG] Full prompt built ({len(full_prompt)} characters)")
        
        result = call_gemini(full_prompt)
        
        pyperclip.copy(result)
        verbose_print("✓ Response copied to clipboard")
        
    except Exception as e:
        debug_print(f"[DEBUG] ERROR: {type(e).__name__}: {str(e)}")
        verbose_print(f"✗ Error: {str(e)}")

def main():
    debug_print(f"[DEBUG] DEBUG mode enabled")
    debug_print(f"[DEBUG] Base prompt file: {PROMPT_BASE_PATH}")
    debug_print(f"[DEBUG] Prompt file: {PROMPT_PATH}")
    debug_print(f"[DEBUG] Hotkey combination: {TXT_HOTKEY_COMBINATION}")
    
    verbose_print(f"Press {TXT_HOTKEY_COMBINATION.upper()} to activate Gemini action from file.")
    verbose_print(f"Press {DIRECT_HOTKEY_COMBINATION.upper()}[prompt base ID] to activate Gemini from clipboard.")

    keyboard.add_hotkey(TXT_HOTKEY_COMBINATION, lambda: threading.Thread(target=handle_action, daemon=True).start())
    
    if DIRECT_HOTKEY_COMBINATION:
        prompt_bases = load_prompt_base()
        
        for prompt_id in prompt_bases.keys():
            hotkey = f"{DIRECT_HOTKEY_COMBINATION}{prompt_id}"
            keyboard.add_hotkey(
                hotkey, 
                lambda pid=prompt_id: threading.Thread(target=handle_direct_action, args=(pid,), daemon=True).start()
            )
            debug_print(f"[DEBUG] Registered hotkey: {hotkey}")
    
    verbose_print("Listening for hotkeys... (Press Ctrl+C to exit)")
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        verbose_print("\nProgram terminated.")

if __name__ == "__main__":
    main()
