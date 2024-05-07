import requests
import re
from datetime import datetime, timedelta

url = 'https://api.github.com/repos/MarlinFirmware/Marlin/commits'
params = {'per_page': 100}  # Set the number of commits per page
response = requests.get(url, params=params)
commits = response.json()

# Calculate the date one week ago
one_week_ago = datetime.now() - timedelta(days=7)  # Changed days to 7 for one week

with open('output_HTML.txt', 'w') as file:
    file.write('<ul>\n')
    while len(commits) > 0:
        for commit in commits:
            if isinstance(commit, dict):
                commit_date_str = commit.get('commit', {}).get('author', {}).get('date')
                if commit_date_str:
                    commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')
                    if commit_date >= one_week_ago and not commit.get('commit', {}).get('message', '').startswith('[cron]'):
                        message = commit['commit']['message'].split('\n')[0]  # Extract the first line as description
                        emoji_match = re.search(r'^([^ ]+)', message)
                        emoji = emoji_match.group(1) if emoji_match else ''
                        commit_id_match = re.search(r'\(#(\d+)\)', message)
                        if commit_id_match:
                            commit_id = commit_id_match.group(1)
                            description = message
                            if emoji and not re.match(r'^[a-zA-Z]+', message):
                                emoji = f'{emoji} '  # Add space after emoji if needed
                            description = re.sub(r'^[^ ]+ ', '', description)  # Remove emoji
                            description = re.sub(r'\s*\([^)]*\)', '', description)  # Remove commit ID
                            file.write(f'<li>{emoji}<a href="https://github.com/MarlinFirmware/Marlin/pull/{commit_id}">{description}</a></li>\n')

        # Check for pagination and fetch the next page of commits
        if 'Link' in response.headers:
            next_url = None
            links = response.headers['Link'].split(',')
            for link in links:
                if 'rel="next"' in link:
                    next_url = link.split(';')[0].strip('<>')
            if next_url:
                response = requests.get(next_url)
                commits = response.json()
            else:
                break
        else:
            break

    file.write('</ul>')
