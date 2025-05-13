from assistant.assistant import AIAssistant
from assistant.llm_prompting import LLMClient
from assistant.helpers import parse_commands_with_comments, display_commands, get_user_confirmation
from assistant.prompts import generate_prompt, regenerate_prompt

llmClient = LLMClient()

def run_commands(assistant, parsed_cmds, step_by_step: bool):
    command_list = [item['command'] for item in parsed_cmds]

    def approval_callback(command, idx):
        description = parsed_cmds[idx]['description'] if idx < len(parsed_cmds) else 'No description available'
        response = input(f"⚠️ Do you want to run this command? \nCommand: {command}\nDescription: {description}\n(y/n): ").strip().lower()
        return response != 'n'

    outputs = assistant.run_commands(command_list, step_by_step=step_by_step, approval_callback=approval_callback if step_by_step else None)

    print("\n🚀 Running Commands...")
    for item, output in zip(parsed_cmds, outputs):
        print(f"🧾 {item['command']}\n➡️ {output}\n")
    return outputs

def retry_logic(user_task, parsed_cmds, outputs, assistant, max_retries=3):
    retry_count = 0

    while retry_count < max_retries:
        if input("❓ Did the commands work correctly? (y/n): ").strip().lower() == 'y':
            print("✅ Task completed successfully.")
            return

        retry_count += 1
        error_description = input("🛠️ Describe what went wrong: ")

        retry_prompt = (
            generate_prompt(user_task) +
            "\n\nPreviously executed commands:\n" +
            '\n'.join([f"{item['command']} → {out}" for item, out in zip(parsed_cmds, outputs)]) +
            f"\n\nThe issue was: {error_description}.\n"
            "Please revise the command list accordingly while still following all original instructions."
        )

        raw_commands = llmClient.prompt_structured_output(retry_prompt)
        parsed_cmds = parse_commands_with_comments(raw_commands)

        display_commands(parsed_cmds)
        if not get_user_confirmation():
            print("❎ Retry cancelled by user.")
            return

        outputs = run_commands(assistant, parsed_cmds, step_by_step=True)

    print("❌ Maximum retries reached. Please verify manually.")
    
def get_commands_for_user_task(user_task, regenerate = False, previous_prompt = None):
    enhanced_prompt = llmClient.prompt(regenerate_prompt(user_task, previous_prompt) 
                                       if regenerate else
                                       generate_prompt(user_task))
    print("\n📌 Enhanced Prompt:\n", enhanced_prompt)

    raw_commands = llmClient.prompt_structured_output(enhanced_prompt)
    parsed_cmds = parse_commands_with_comments(raw_commands)

    display_commands(parsed_cmds)
    return raw_commands, parsed_cmds
    

def main():
    assistant = AIAssistant()
    user_task = input("💬 What task do you want to automate with command prompt?: ").strip()
    
    (raw_commands, parsed_cmds) = get_commands_for_user_task(user_task)

    if not get_user_confirmation():
        if not get_user_confirmation("⚠️ Do you want to change anything? (y/n):"):
            print("❎ Cancelled by user.")
            return
        user_task_2 = input("💬 Please enter what you need to change in the automation: ").strip()
        (raw_commands, parsed_cmds) = get_commands_for_user_task('1.\n' + user_task + 
                                                 '2.\n' + user_task_2, 
                                                 True, raw_commands)
        

    step_mode = input("🔁 Do you want to run commands one-by-one interactively? (y/n): ").strip().lower() == 'y'

    outputs = run_commands(assistant, parsed_cmds, step_by_step=step_mode)
    retry_logic(user_task, parsed_cmds, outputs, assistant)

if __name__ == "__main__":
    main()
