import subprocess
import os
from datetime import datetime

# GitHub repository path
repo_dir = '/home/ubuntu/finalproject'

# Log the status of the job
log_file = '/home/ubuntu/finalproject/logs/scraping.log'
log_message = f"{datetime.now()} - Job and Event scraping completed successfully.\n"

# Append log message to the file
with open(log_file, 'a') as f:
    f.write(log_message)

# Commit and push to GitHub
os.chdir(repo_dir)
subprocess.run(['git', 'add', 'logs/scraping.log'])
subprocess.run(['git', 'commit', '-m', 'Updated scraping log'])
subprocess.run(['git', 'push', 'origin', 'master'])
