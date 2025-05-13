import os
import openai
import subprocess
from dotenv import load_dotenv
from google import genai

load_dotenv()

model_type = 'gemini'
model_name = 'gemini-2.0-flash'

class LLMClient:
    def __init__(self):
        self.llm_client = None
        self.model_type = model_type.lower()
        self.model_name = model_name
        self.api_key = None

        if self.model_type == 'openai':
            pass
        elif self.model_type == 'gemini':
            self.api_key = os.getenv("GOOGLE_API_KEY")
            self.llm_client = genai.Client(api_key=self.api_key)
        elif self.model_type == 'ollama':
            # Ollama uses CLI, no SDK initialization needed
            pass
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")

    def prompt(self, prompt_text):
        if self.model_type == 'openai':
            response = openai.Completion.create(
                model=self.model_name or "gpt-3.5-turbo",
                prompt=prompt_text,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        elif self.model_type == 'gemini':
            response = self.llm_client.models.generate_content(
                model=model_name, contents=prompt_text
            )
            return response.text
        elif self.model_type == 'ollama':
            try:
                result = subprocess.run(
                    ["ollama", "query", self.model_name or "llama2", prompt_text],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    return f"Ollama CLI error: {result.stderr.strip()}"
            except Exception as e:
                return f"Ollama CLI exception: {str(e)}"
        else:
            raise ValueError(f"Unsupported model_type: {self.model_type}")

    def prompt_structured_output(self, prompt_text):
        if self.model_type == 'openai':
            response = openai.Completion.create(
                model=self.model_name or "gpt-3.5-turbo",
                prompt=prompt_text,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        elif self.model_type == 'gemini':
            response = self.llm_client.models.generate_content(
                model=model_name, 
                contents=prompt_text,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': { "type": "array", "items": { "type": "string" } }
                },
            )
            return response.parsed
        elif self.model_type == 'ollama':
            try:
                result = subprocess.run(
                    ["ollama", "query", self.model_name or "llama2", prompt_text],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    return f"Ollama CLI error: {result.stderr.strip()}"
            except Exception as e:
                return f"Ollama CLI exception: {str(e)}"
        else:
            raise ValueError(f"Unsupported model_type: {self.model_type}")
