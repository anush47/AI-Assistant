def parse_commands_with_comments(command_list):
    parsed = []
    for line in command_list:
        if '& rem' in line:
            cmd, comment = line.split('& rem', 1)
            parsed.append({'command': cmd.strip(), 'description': comment.strip()})
        else:
            parsed.append({'command': line.strip(), 'description': 'No description provided'})
    return parsed

def display_commands(parsed_cmds):
    print("\n📋 Command Preview with Descriptions:")
    for i, item in enumerate(parsed_cmds, 1):
        print(f"{i}. 🧾 {item['command']}\n   📘 {item['description']}\n")

def get_user_confirmation(prompt="⚠️ Do you want to proceed? (y/n): ") -> bool:
    return input(prompt).strip().lower() == 'y'
