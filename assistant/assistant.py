import pyautogui
import subprocess
import time
from typing import List, Union
from PIL import Image
import pytesseract
import difflib

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class AIAssistant:
    def __init__(self, pause: float = 0.1):
        pyautogui.PAUSE = pause
        pyautogui.FAILSAFE = True
        
    def run_commands(self, commands: list[str], shell: bool = True, timeout: int = 30, step_by_step: bool = False, approval_callback=None) -> list[str]:
        outputs = []

        if step_by_step:
            # Run each command separately but in the same shell session with user approval
            shell_context = subprocess.Popen("cmd", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            for idx, command in enumerate(commands):
                try:
                    if approval_callback:
                        # Pass both command and description (if available) to approval_callback
                        approved = approval_callback(command, idx)
                        if not approved:
                            outputs.append("Skipped by user.")
                            continue

                    shell_context.stdin.write(command + "\n")
                    shell_context.stdin.flush()
                    shell_context.stdin.write("echo ___END___\n")  # Marker
                    shell_context.stdin.flush()

                    output = ""
                    while True:
                        line = shell_context.stdout.readline()
                        if "___END___" in line:
                            break
                        output += line
                    outputs.append(output.strip())
                except Exception as e:
                    outputs.append(f"Error executing command: {e}")
            shell_context.stdin.write("exit\n")
            shell_context.stdin.flush()
        else:
            # Run all commands in one go (joined with &&)
            try:
                command_string = " && ".join(commands)
                completed = subprocess.run(command_string, shell=shell, capture_output=True, text=True, timeout=timeout)
                output = completed.stdout.strip()
                error = completed.stderr.strip()
                outputs.append(f"{output}\n{error}".strip() if error else output)
            except subprocess.TimeoutExpired:
                outputs.append("Command timed out.")
            except Exception as e:
                outputs.append(f"Error executing commands: {e}")

        return outputs

    def move_mouse(self, x: int, y: int, duration: float = 0.25):
        pyautogui.moveTo(x, y, duration=duration)

    def move_mouse_relative(self, dx: int, dy: int, duration: float = 0.25):
        pyautogui.moveRel(dx, dy, duration=duration)

    def click(self, x: Union[int, None] = None, y: Union[int, None] = None, button: str = 'left', clicks: int = 1, interval: float = 0.0):
        if x is not None and y is not None:
            pyautogui.click(x=x, y=y, clicks=clicks, interval=interval, button=button)
        else:
            pyautogui.click(clicks=clicks, interval=interval, button=button)

    def double_click(self, x: Union[int, None] = None, y: Union[int, None] = None, button: str = 'left'):
        self.click(x, y, button=button, clicks=2, interval=0.1)

    def right_click(self, x: Union[int, None] = None, y: Union[int, None] = None):
        self.click(x, y, button='right')

    def press_key(self, key: str):
        pyautogui.press(key)

    def press_keys(self, keys: List[str], interval: float = 0.1):
        for key in keys:
            pyautogui.keyDown(key)
            time.sleep(interval)
        time.sleep(interval)
        [pyautogui.keyUp(key) for key in keys]

    def hotkey(self, *keys: str):
        pyautogui.hotkey(*keys)

    def type_text(self, text: str, interval: float = 0.05):
        pyautogui.write(text, interval=interval)
        
    def get_screen_size(self):
        return pyautogui.size()

    def screenshot(self, path: str = None):
        screenshot = pyautogui.screenshot()
        if path:
            screenshot.save(path)
        return screenshot

    def get_screen_content_with_position(self):
        screenshot = self.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        results = []
        n_boxes = len(data['level'])
        for i in range(n_boxes):
            text = data['text'][i].strip()
            if text:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                results.append({'text': text, 'box': (x, y, w, h)})
        return results

    def find_closest_matches_from_screen(self, query: str, n: int = 3, cutoff: float = 0.6) -> List[dict]:
        screen_content = self.get_screen_content_with_position()
        texts = [item['text'] for item in screen_content]
        closest_texts = difflib.get_close_matches(query, texts, n=n, cutoff=cutoff)
        matches = [item for item in screen_content if item['text'] in closest_texts]
        return matches
