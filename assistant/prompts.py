def generate_prompt(user_task: str) -> str:
    return (
        "Generate the minimal and correct list of Windows Command Prompt commands required to complete this task: "
        f"\"{user_task}\". Only include the most effective, reliable approach — do not provide multiple alternatives. "
        "Each command must include a short inline comment using '& rem' that explains what the command does. "
        "Ensure the format is a valid Python list of strings like: "
        "[\"command1 & rem description\", \"command2 & rem description\"] and so on. "
        "Avoid unnecessary steps. Use only one browser or one method unless multiple steps are strictly required. "
        "If any command might have security risks, add a warning in the '& rem' comment. "
        "Be precise, brief, and prioritize safe execution."
    )
    
def regenerate_prompt(user_task: str, previous_prompt: str) -> str:
    return (
        "Generate the minimal and correct list of Windows Command Prompt commands required to complete this task: "
        f"\"{user_task}\". Only include the most effective, reliable approach — do not provide multiple alternatives. "
        "Each command must include a short inline comment using '& rem' that explains what the command does. "
        "Ensure the format is a valid Python list of strings like: "
        "[\"command1 & rem description\", \"command2 & rem description\"] and so on. "
        "Avoid unnecessary steps. Use only one browser or one method unless multiple steps are strictly required. "
        "If any command might have security risks, add a warning in the '& rem' comment. "
        "Be precise, brief, and prioritize safe execution."
        f"Previously generated prompt was: \"{previous_prompt}\""
        "modify this to achieve the given task."
        "finally output the Complete list of commands that needs to be executed"
    )
