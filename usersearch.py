import sys
import requests
import pandas as pd
import time

GITHUB_TOKEN = 'your_token_here'  # Replace or load from environment
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}

def get_username_from_url(url):
    return url.strip('/').split('/')[-1]

def get_repositories(username):
    repos = []
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/users/{username}/repos',
            headers=HEADERS,
            params={'per_page': 100, 'page': page}
        )
        if response.status_code != 200:
            print(f"⚠️ Could not fetch repos for {username} (status {response.status_code})")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def search_keywords_in_repo(repo, keywords):
    text = (repo.get('name', '') + ' ' + str(repo.get('description', ''))).lower()
    for keyword in keywords:
        if keyword.lower() in text:
            return True, repo.get('html_url')
    return False, None

def search_code(username, keywords):
    for keyword in keywords:
        query = f"{keyword} user:{username}"
        response = requests.get(
            "https://api.github.com/search/code",
            headers=HEADERS,
            params={"q": query, "per_page": 1}
        )
        if response.status_code == 200:
            items = response.json().get("items", [])
            if items:
                return True, items[0].get('html_url')
        elif response.status_code == 403:
            print("⚠️ Rate limit hit, sleeping 60 seconds...")
            time.sleep(60)
        time.sleep(1)
    return False, None

def main(input_csv):
    keyword_input = input("Enter keywords to search (comma-separated): ")
    KEYWORDS = [kw.strip().lower() for kw in keyword_input.split(',') if kw.strip()]
    if not KEYWORDS:
        print("❌ No valid keywords entered. Exiting.")
        return

    df = pd.read_csv(input_csv)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    if 'profile_url' not in df.columns or 'username' not in df.columns:
        print("❌ CSV must contain at least 'Username' and 'Profile URL'")
        print("Your columns:", df.columns.tolist())
        return

    results = []

    for _, row in df.iterrows():
        query = row.get('query', '')
        fullname = row.get('full_name', '')
        username = row['username']
        profile_url = row['profile_url']

        display_name = fullname if pd.notna(fullname) else query
        print(f"🔍 Checking {display_name} ({username})")

        matched = False
        matched_url = None

        repos = get_repositories(username)
        for repo in repos:
            repo_match, url = search_keywords_in_repo(repo, KEYWORDS)
            if repo_match:
                matched = True
                matched_url = url
                break

        if not matched:
            code_match, url = search_code(username, KEYWORDS)
            if code_match:
                matched = True
                matched_url = url

        if matched:
            results.append({
                'fullname': display_name,
                'username': username,
                'profile_url': f'https://github.com/{username}',
                'matched_url': matched_url
            })

    output_df = pd.DataFrame(results)
    output_df.to_csv('user_matches.csv', index=False)
    print("✅ Done! Matches saved to user_matches.csv")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python usersearch.py users.csv")
        sys.exit(1)
    main(sys.argv[1])
