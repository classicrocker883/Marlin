import requests
import re

url = 'https://api.github.com/repos/MarlinFirmware/Marlin/commits'
response = requests.get(url)
commits = response.json()

with open('output_HTML.txt', 'w') as file:
    file.write('<ul>\n')
    for commit in commits:
        message = commit['commit']['message']
        if not message.startswith('[cron]'):
            emoji_match = re.search(r'^([^ ]+)', message)
            emoji = emoji_match.group(1) if emoji_match else ''
            commit_id_match = re.search(r'\(#(\d+)\)', message)
            if commit_id_match:
                commit_id = commit_id_match.group(1)
                description = re.sub(r'^[^ ]+ ', '', message)  # Remove emoji
                description = re.sub(r'\s*\([^)]*\)', '', description)  # Remove commit ID
                file.write(f'<li>{emoji} <a href="https://github.com/MarlinFirmware/Marlin/pull/{commit_id}">{description}</a></li>\n')
    file.write('</ul>')
