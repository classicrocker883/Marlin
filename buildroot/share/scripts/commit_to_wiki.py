#!/usr/bin/env python3

import os

# Define the path to output_HTML_commits.txt within the workspace directory
output_commits_path = 'output_HTML_commits.txt'
print(f"is '{os.path.abspath(output_commits_path)}' is output_HTML_commits.txt.")

# Read the contents of output_HTML_commits.txt
with open(output_commits_path, 'r') as file1:
    file1_content = file1.readlines()

# Define the file name with the special character
file_name = "New‐in‐this‐Release.md"  # Make sure to use the correct special character

wiki_file_path = os.path.join('..', '..', '..', 'wiki')
print(f"is '{os.path.abspath(wiki_file_path)}'  wiki directory.")

# Define the path to New-in-this-Release.md within the workspace directory
release_notes_path = os.path.abspath(os.path.join(wiki_file_path, file_name))

if not os.path.exists(release_notes_path):
    print(f"Error: New-in-this-Release.md not found at wiki")
    exit(1)
# # with open("https://raw.githubusercontent.com/wiki/classicrocker883/MRiscoCProUI/New-in-this-Release.md", 'r') as file2:
# #     file2_content = file2.readlines()

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


