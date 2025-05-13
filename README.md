# AI Assistant Command Automation

This project is a Python-based AI assistant that helps automate command-line tasks by generating shell commands using large language models (LLMs) such as OpenAI and Google GenAI. The assistant interacts with the user to understand the task, generates commands, and optionally runs them step-by-step with user approval.

## Features

- Uses Google GenAI APIs to generate commands based on user input.
- Supports interactive step-by-step command execution with user confirmation.
- Allows retrying and refining commands if the initial execution does not work as expected.
- Currently optimized to utilize Windows command prompt, Support for linux will be added soon.

## Prerequisites

- Python 3.7 or higher
- API keys for OpenAI and Google GenAI (set in environment variables or a `.env` file)

## Installation

1. Clone the repository or download the project files.

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   venv\\Scripts\\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   Create a `.env` file in the project root with your API keys, for example:

   ```
   GOOGLE_GENAI_API_KEY=your_google_genai_api_key_here
   ```

## Usage

Run the main application script:

```bash
python app.py
```

You will be prompted to enter the task you want to automate. The assistant will generate commands and ask for your confirmation before running them. You can choose to run commands step-by-step or all at once. If the commands do not work as expected, you can retry with revised instructions.

## Project Structure

- `app.py`: Main entry point of the application.
- `requirements.txt`: Python dependencies.
- `assistant/`: Contains core modules for LLM prompting, command parsing, and assistant logic.

## License

This project is provided as-is without any warranty. Use it responsibly.

## Future Plans

- OpenAI / Ollama integration
- GUI interactions are under development.
- Integrate automation and OCR libraries like pyautogui, pytesseract for enhanced capabilities.
- Capability for voice commands
