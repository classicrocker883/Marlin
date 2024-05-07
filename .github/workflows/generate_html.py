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
            if '(#' in message:
                commit_id = re.search(r'\(#(\d+)\)', message).group(1)
                file.write(f'<li>{emoji} <a href="https://github.com/MarlinFirmware/Marlin/pull/{commit_id}">{message}</a></li>\n')
            else:
                file.write(f'<li>{emoji} {message}</li>\n')
    file.write('</ul>')
