import subprocess
import time

class AIAssistant:
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
