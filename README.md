# TransparentChat

A hotkey-activated AI assistant that integrates Google Gemini API with customizable prompts. Press a keyboard shortcut to process predefined prompts and get AI-generated responses directly to your clipboard.

## 📑 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#-usage)
  - [Mode 1: File-Based Prompts](#mode-1-file-based-prompts)
  - [Mode 2: Direct Clipboard Prompts](#mode-2-direct-clipboard-prompts)
  - [Base Prompts](#base-prompts)
  - [Workflow Examples](#workflow-examples)
- [Configuration](#️-configuration)
  - [Environment Variables](#environment-variables)
  - [Logging Modes](#logging-modes)
  - [Hotkey Combinations](#hotkey-combinations)
- [Project Structure](#️-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## 🌟 Features

- **Dual Hotkey Modes**: 
  - File-based prompts (read from text file)
  - Direct clipboard prompts (process clipboard content)
- **Hotkey Activation**: Trigger AI processing with customizable keyboard shortcuts
- **Modular Prompts**: Use base prompt templates combined with specific queries
- **Clipboard Integration**: Responses are automatically copied to your clipboard
- **Configurable**: Easy setup via `.env` file
- **Debug & Verbose Modes**: Separate controls for detailed logging and user messages
- **Cross-platform**: Support for Windows, mainly tested on Windows 11. Future Linux support is planned

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TransparentChat.git
   cd TransparentChat
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Gemini API Configuration
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-2.5-flash-lite

   # Prompt file configuration
   PROMPT_PATH=C:\path\to\your\
   PROMPT_NAME=prompt.txt

   # Hotkey configuration
   TXT_HOTKEY_COMBINATION=ctrl+shift+o
   DIRECT_HOTKEY_COMBINATION=ctrl+shift+d+

   # Logging configuration
   DEBUG=false
   VERBOSE=true
   ```

5. **Run the application**

    **Windows**: double-click the [`run_as_admin.bat`](Windows/run_as_admin.bat) file to start the application with administrator privileges.
    ```bash
    Windows\run_as_admin.bat
    ```

## 📖 Usage

### Mode 1: File-Based Prompts

1. Create a text file at the location specified in `PROMPT_PATH` + `PROMPT_NAME`

2. Format your prompt file:
   ```
   1. [text not taken into account]
   Additional details or specific question...
   ```
   
   The first character must be a digit (1-9) that corresponds to a prompt base ID from [`prompt_base.json`](prompt_base.json). The rest of the file is appended to the base prompt. By now only single-digit IDs are supported.

3. Press the hotkey combination defined in `TXT_HOTKEY_COMBINATION` (default: `Ctrl+Shift+O`)

### Mode 2: Direct Clipboard Prompts

1. Copy your specific question or details to the clipboard

2. Press the hotkey combination defined in `DIRECT_HOTKEY_COMBINATION` followed by the prompt base ID digit (e.g., `Ctrl+Shift+D+1`). The final digit corresponds to a prompt base ID from [`prompt_base.json`](prompt_base.json).

### Base Prompts

Edit [`prompt_base.json`](prompt_base.json) to define reusable prompt templates:

```json
[
    {
        "id": 1,
        "name": "Python code question",
        "content": "Help me write a Python script (.py file) based on the characteristics I'll provide. Only respond with the script, no explanations or comments.\nProblem characteristics:\n"
    },
    {
        "id": 2,
        "name": "Development question",
        "content": "Provide a text-based answer (maximum 70 words) to the question and data I'll provide. Only respond with text, no code or additional explanations.\nQuestion:\n"
    }
]
```

### Workflow Examples

**File-Based Workflow:**
1. Write your prompt in the configured prompt file
2. Press the hotkey combination (default: `Ctrl+Shift+O`)
3. Wait for processing (check terminal for debug messages if enabled)
4. Paste the AI response from your clipboard (`Ctrl+V`)

**Direct Clipboard Workflow:**
1. Copy text to clipboard (`Ctrl+C`)
2. Press `Ctrl+Shift+D+1` (or any prompt base ID)
3. Wait for processing
4. Paste the AI response from your clipboard (`Ctrl+V`)

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | - | ✅ Yes |
| `GEMINI_MODEL` | Gemini model to use | `gemini-2.5-flash-lite` | No |
| `PROMPT_PATH` | Directory path for prompt file | - | ✅ Yes (for file mode) |
| `PROMPT_NAME` | Name of the prompt file | - | ✅ Yes (for file mode) |
| `TXT_HOTKEY_COMBINATION` | Keyboard shortcut for file-based prompts | `ctrl+shift+o` | No |
| `DIRECT_HOTKEY_COMBINATION` | Base keyboard shortcut for clipboard prompts | `ctrl+shift+d+` | No |
| `DEBUG` | Enable detailed debug logging | `false` | No |
| `VERBOSE` | Enable user-facing messages | `true` | No |

### Logging Modes

- **`VERBOSE=true, DEBUG=false`** (Recommended): Shows main status messages (start, success, errors)
- **`VERBOSE=true, DEBUG=true`** (Development): Shows all messages including technical details
- **`VERBOSE=false, DEBUG=false`** (Silent): Minimal output, only critical errors
- **`VERBOSE=false, DEBUG=true`**: Debug messages only when verbose is enabled

### Hotkey Combinations

You can use any valid keyboard combination. Examples:
- `ctrl+shift+o`
- `ctrl+alt+g`
- `shift+f1`
- `ctrl+shift+alt+a`

For `DIRECT_HOTKEY_COMBINATION`, add a `+` at the end:
- `ctrl+shift+d+` → Press `Ctrl+Shift+D+1`, `Ctrl+Shift+D+2`, etc.
- `alt+p+` → Press `Alt+P+1`, `Alt+P+2`, etc.

## 🛠️ Project Structure

```
TransparentChat/
├── Windows/
│   ├── main.py              # Main application script
│   ├── run_as_admin.bat     # Run with admin privileges (Windows)
│   └── __pycache__/
├── Linux/                   # Linux-specific files (future)
├── prompt_base.json         # Base prompt templates
├── prompt_base_final.json   # Alternative prompt templates
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration (not in repo)
├── .gitignore
├── LICENSE
└── README.md
```

## 🐛 Troubleshooting

### Common Issues

**Hotkey not working:**
- Run the script with administrator privileges (use [`run_as_admin.bat`](Windows/run_as_admin.bat) on Windows)
- Check that another application isn't using the same hotkey
- Try a different hotkey combination
- Enable `VERBOSE=true` to see confirmation messages

**API errors:**
- Verify your `GEMINI_API_KEY` is valid
- Check your internet connection
- Ensure you haven't exceeded API rate limits

**File not found errors:**
- Verify `PROMPT_PATH` and `PROMPT_NAME` are correct in [`.env`](.env)
- Use absolute paths in `PROMPT_PATH`
- Check file permissions

**Clipboard is empty (direct mode):**
- Ensure you have copied text before pressing the hotkey
- Try copying again and retry

**Enable Debug Mode:**
Set `DEBUG=true` and `VERBOSE=true` in your [`.env`](.env) file to see detailed logs.

## 📝 Examples

### File-Based Mode

**ai_prompt.txt:**
```
1
Calculate the mean and standard deviation for a variable called "income" and create a histogram
```

Press `Ctrl+Shift+O` → Generated Stata code is copied to clipboard

### Direct Clipboard Mode

**Clipboard content:**
```
Calculate the mean and standard deviation for a variable called "income" and create a histogram
```

Press `Ctrl+Shift+D+1` → Generated Stata code is copied to clipboard

---

**Clipboard content:**
```
¿Qué es la economía positiva y cómo se diferencia de la economía normativa?
```

Press `Ctrl+Shift+D+2` → Generated text answer is copied to clipboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev/)
- Uses [keyboard](https://github.com/boppreh/keyboard) for hotkey detection
- Uses [pyperclip](https://github.com/asweigart/pyperclip) for clipboard operations
- Uses [python-dotenv](https://github.com/theskumar/python-dotenv) for environment configuration

---

**Note:** This tool is designed for personal productivity and educational purposes. Always review AI-generated content before use.
