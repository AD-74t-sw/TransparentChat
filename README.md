# TransparentChat

A hotkey-activated AI assistant that integrates Google Gemini API with customizable prompts. Press a keyboard shortcut to process predefined prompts and get AI-generated responses directly to your clipboard.

## 🌟 Features

- **Hotkey Activation**: Trigger AI processing with a customizable keyboard shortcut
- **Modular Prompts**: Use base prompt templates combined with specific queries
- **Clipboard Integration**: Responses are automatically copied to your clipboard
- **Configurable**: Easy setup via `.env` file
- **Debug Mode**: Optional verbose logging for troubleshooting
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
   HOTKEY_COMBINATION=ctrl+shift+o

   # Debug mode
   DEBUG=false
   ```

5. **Run the application**

    **Windows**: double-click the `run_as_admin.bat` file to start the application with administrator privileges.
    ```bash
    run_as_admin.bat
    ```

## 📖 Usage

### Creating Prompts

1. Create a text file at the location specified in `PROMPT_PATH` + `PROMPT_NAME`

2. Format your prompt file:
   ```
   1. [text not taken into account]
   Additional details...
   ```
   
   The first character must be a digit (1-9) that corresponds to a prompt base ID from `prompt_base.json`. By now only single-digit IDs are supported.

### Base Prompts

Edit `prompt_base.json` to define reusable prompt templates:

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
        "content": "Provide a text-based answer to the question and data I'll provide. Only respond with text, no code or additional explanations.\nQuestion:\n"
    }
]
```

### Workflow

1. Write your prompt in the configured prompt file
2. Press the hotkey combination (default: `Ctrl+Shift+O`)
3. Wait for processing (check terminal for debug messages if enabled)
4. Paste the AI response from your clipboard (`Ctrl+V`)

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | - | ✅ Yes |
| `GEMINI_MODEL` | Gemini model to use | `gemini-2.5-flash-lite` | No |
| `PROMPT_PATH` | Directory path for prompt file | - | ✅ Yes |
| `PROMPT_NAME` | Name of the prompt file | - | ✅ Yes |
| `HOTKEY_COMBINATION` | Keyboard shortcut to activate | `ctrl+shift+o` | No |
| `DEBUG` | Enable debug logging | `false` | No |

### Hotkey Combinations

You can use any valid keyboard combination. Examples:
- `ctrl+shift+o`
- `ctrl+alt+g`
- `shift+f1`
- `ctrl+shift+alt+a`

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
└── README.md
```

## 🐛 Troubleshooting

### Common Issues

**Hotkey not working:**
- Run the script with administrator privileges (use `run_as_admin.bat` on Windows)
- Check that another application isn't using the same hotkey
- Try a different hotkey combination

**API errors:**
- Verify your `GEMINI_API_KEY` is valid
- Check your internet connection
- Ensure you haven't exceeded API rate limits

**File not found errors:**
- Verify `PROMPT_PATH` and `PROMPT_NAME` are correct in `.env`
- Use absolute paths in `PROMPT_PATH`
- Check file permissions

**Enable Debug Mode:**
Set `DEBUG=true` in your `.env` file to see detailed logs.

## 📝 Example

**ai_prompt.txt:**
```
1
Calculate the mean and standard deviation for a variable called "income" and create a histogram
```

**Result:**
Press `Ctrl+Shift+O`, and the generated Stata code is copied to your clipboard.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev/)
- Uses [keyboard](https://github.com/boppreh/keyboard) for hotkey detection
- Uses [pyperclip](https://github.com/asweigart/pyperclip) for clipboard operations

---

**Note:** This tool is designed for personal productivity and educational purposes. Always review AI-generated content before use.
