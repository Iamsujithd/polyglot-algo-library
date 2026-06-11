import os
import sys
import json
import random
import time
import urllib.request
import subprocess
from datetime import datetime

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TRACKER_FILE = "scripts/tracker.json"
MAX_DAILY_COMMITS = 20

def get_today_str():
    return datetime.utcnow().strftime("%Y-%m-%d")

def read_tracker():
    if not os.path.exists(TRACKER_FILE):
        return {"date": get_today_str(), "count": 0}
    with open(TRACKER_FILE, "r") as f:
        data = json.load(f)
        if data.get("date") != get_today_str():
            return {"date": get_today_str(), "count": 0}
        return data

def write_tracker(count):
    with open(TRACKER_FILE, "w") as f:
        json.dump({"date": get_today_str(), "count": count}, f)

def execute_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}\nError: {result.stderr}")
    return result.stdout.strip()

def generate_contribution():
    prompt = """
You are a developer building a Polyglot Algorithms Library in Python and Java.
Write a small, simple algorithm, data structure, or unit test.
Choose either Python (.py) or Java (.java).
Keep the code UNDER 50 lines to save tokens.
Return ONLY valid JSON in this exact format:
{
  "filepath": "python/math/fibonacci.py",
  "content": "def fib(n):...",
  "commit_message": "feat: add iterative fibonacci implementation"
}
"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
        "response_format": {"type": "json_object"}
    }
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", headers=headers, method="POST")
    req.data = json.dumps(data).encode("utf-8")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode())
            content = res_json['choices'][0]['message']['content']
            return json.loads(content)
    except urllib.error.HTTPError as e:
        print(f"API Error: HTTP Error {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"API Error: {e}")
        return None

def main():
    if not GROQ_API_KEY:
        print("Missing GROQ_API_KEY")
        sys.exit(1)

    # 1. 60% chance to do completely nothing (simulating being offline)
    if random.random() < 0.60:
        print("Skipping this hour to simulate natural gaps.")
        sys.exit(0)

    # 2. Check daily limit
    tracker = read_tracker()
    if tracker["count"] >= MAX_DAILY_COMMITS:
        print("Daily limit reached.")
        sys.exit(0)

    # 3. Random sleep up to 45 minutes to avoid committing exactly on the hour
    sleep_time = random.randint(1, 2700)
    print(f"Sleeping for {sleep_time} seconds before committing...")
    time.sleep(sleep_time)

    # 4. Decide how many commits to make right now (1 to 3)
    commits_to_make = random.randint(1, 3)
    
    for _ in range(commits_to_make):
        if tracker["count"] >= MAX_DAILY_COMMITS:
            break
            
        print("Generating contribution...")
        contrib = generate_contribution()
        if not contrib:
            continue
            
        filepath = contrib.get("filepath")
        content = contrib.get("content")
        commit_message = contrib.get("commit_message")
        
        if not filepath or not content:
            continue
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        
        with open(filepath, "w") as f:
            f.write(content)
            
        # Git operations
        execute_cmd(f'git add "{filepath}"')
        execute_cmd('git add scripts/tracker.json')
        execute_cmd(f'git commit -m "{commit_message}"')
        
        tracker["count"] += 1
        write_tracker(tracker["count"])
        
        print(f"Committed: {commit_message}")
        
        # Sleep briefly between commits in the same batch
        time.sleep(random.randint(10, 60))

    # Push all changes
    execute_cmd("git push origin main")
    print(f"Pushed to GitHub. Total commits today: {tracker['count']}")

if __name__ == "__main__":
    main()
