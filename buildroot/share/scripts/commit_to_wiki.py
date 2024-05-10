#!/usr/bin/env python3

import os

# Define the path to output_HTML_commits.txt within the workspace directory
output_commits_path = os.path.join(os.getenv('GITHUB_WORKSPACE'), 'buildroot', 'share', 'scripts', 'output_HTML_commits.txt')

# Check if output_HTML_commits.txt exists
if not os.path.exists(output_commits_path):
    print(f"Error: output_HTML_commits.txt not found at {output_commits_path}")
    print("Falling back to default path...")
    output_commits_path = 'buildroot/share/scripts/output_HTML_commits.txt'

if not os.path.exists(output_commits_path):
    print(f"Error: output_HTML_commits.txt not found at buildroot/share/scripts")
    exit(1)

# Read the contents of output_HTML_commits.txt
with open(output_commits_path, 'r') as file1:
    file1_content = file1.readlines()

# Define the path to New-in-this-Release.md within the workspace directory
release_notes_path = os.path.join(os.getenv('GITHUB_WORKSPACE'), 'wiki', 'New-in-this-Release.md')

# Define the path to the directory you want to check
wiki_path = os.path.join(os.getenv('GITHUB_WORKSPACE'), 'wiki')

# List the contents of the directory
print(f"Contents of the directory: {wiki_path}")
wiki_contents = os.listdir(wiki_path)
for item in wiki_contents:
    print(item)

# Check if the file 'New-in-this-Release.md' is present
if 'New-in-this-Release.md' in wiki_contents:
    print("File 'New-in-this-Release.md' found in the directory.")
else:
    print("File 'New-in-this-Release.md' not found in the directory.")

# Define the path to the GITHUB_WORKSPACE directory
workspace_path = os.getenv('GITHUB_WORKSPACE')

# List the contents of the GITHUB_WORKSPACE directory
print(f"Contents of the GITHUB_WORKSPACE directory: {workspace_path}")
workspace_contents = os.listdir(workspace_path)
for item in workspace_contents:
    print(item)

# Check if the file 'New-in-this-Release.md' is present in the GITHUB_WORKSPACE directory
if 'New-in-this-Release.md' in workspace_contents:
    print("File 'New-in-this-Release.md' found in the GITHUB_WORKSPACE directory.")
else:
    print("File 'New-in-this-Release.md' not found in the GITHUB_WORKSPACE directory.")

def find_file(start_dir, target_file):
    for root, dirs, files in os.walk(start_dir):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

# Define the path to the GITHUB_WORKSPACE directory
workspace_path = os.getenv('GITHUB_WORKSPACE')

# Search for the file 'New-in-this-Release.md' within the GITHUB_WORKSPACE directory
file_path = find_file(workspace_path, 'New-in-this-Release.md')

if file_path:
    print(f"File 'New-in-this-Release.md' found at: {file_path}")
else:
    print("File 'New-in-this-Release.md' not found in the GITHUB_WORKSPACE directory.")



# Check if New-in-this-Release.md exists
if not os.path.exists(release_notes_path):
    print(f"Error: New-in-this-Release.md not found at {release_notes_path}")
    print("Falling back to default path...")
    release_notes_path = "wiki/New-in-this-Release.md"

if not os.path.exists(release_notes_path):
    print(f"Error: New-in-this-Release.md not found at wiki")
    exit(1)
# with open("https://raw.githubusercontent.com/wiki/classicrocker883/MRiscoCProUI/New-in-this-Release.md", 'r') as file2:
#     file2_content = file2.readlines()

# Read the content of New-in-this-Release.md
with open(release_notes_path, 'r') as file2:
    file2_content = file2.readlines()

# Find the position of <ul> in New-in-this-Release.md
ul_index = next((i for i, line in enumerate(file2_content) if '<ul>' in line), None)

# Extract existing commits from New-in-this-Release.md
existing_commits = [line.strip() for line in file2_content if '<li>' in line]

# Merge the contents of output_HTML_commits.txt with New-in-this-Release.md, omitting duplicates
new_commits = [line for line in file1_content if '<li>' in line and line.strip() not in existing_commits]

# Insert the new content after <ul> in the correct order and without duplicates
if ul_index is not None:
    merged_content = file2_content[:ul_index + 1] + new_commits + file2_content[ul_index + 1:]
else:
    merged_content = file2_content + new_commits  # If <ul> is not found, append at the end

# Write the merged content back to New-in-this-Release.md
with open(release_notes_path, 'w') as file2:
    file2.writelines(merged_content)


