import requests
import re
from datetime import datetime, timedelta
import emoji

def fetch_commits(url, params):
    commits = []
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                break
            commits.extend(data)
            if 'Link' in response.headers:
                links = response.headers['Link'].split(',')
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(';')[0].strip('<>')
                        break
                else:
                    break
            else:
                break
        else:
            print(f"Failed to fetch commits: {response.status_code}")
            break
    return commits

url = 'https://api.github.com/repos/MarlinFirmware/Marlin/commits'
params = {'per_page': 100, 'since': (datetime.now() - timedelta(days=250)).isoformat()}  # Increase per_page to fetch more commits per request
commits = fetch_commits(url, params)

with open('output_HTML_commits.txt', 'w', encoding='utf-8') as file:
    file.write('<ul>\n')
    for commit in commits:
        commit_date_str = commit.get('commit', {}).get('author', {}).get('date')
        if commit_date_str:
            commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')
            if commit_date >= (datetime.now() - timedelta(days=250)) and not commit.get('commit', {}).get('message', '').startswith('[cron]'):
                message = commit['commit']['message'].split('\n')[0]  # Extract the first line as description
                emojis = emoji.emoji_list(message)  # Use emoji_list to get only distinct emojis
                emojis_list = [emoji_data['emoji'] for emoji_data in emojis]  # Extract emojis from the list of emoji data
                emoji_str = ''.join(emojis_list)  # Convert emojis to string
                message = message.replace(emoji_str, '', len(emojis_list))  # Remove the emojis from the message
                commit_id_match = re.search(r'\(#(\d+)\)', message)
                if commit_id_match:
                    commit_id = commit_id_match.group(1)
                    description = message
                    description = description.lstrip()  # Remove leading whitespace
                    description = re.sub(r'\s*\([^)]*\)', '', description)  # Remove commit ID
                    file.write(f'<li>{emoji_str} <a href="https://github.com/MarlinFirmware/Marlin/pull/{commit_id}">{description}</a></li>\n')
                else:
                    file.write(f'<li>{emoji_str}{message}</a></li>\n')  # Include emoji and description without commit ID

    file.write('</ul>')
