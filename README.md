# 🔍 GitHub User Keyword Scanner

Search GitHub users for keywords in their **repositories** or **code** using a CSV list of profiles.

This tool reads a `.csv` file with GitHub user info, prompts you for keywords, and outputs a CSV of matching users along with the link to where the keyword was found.

---

## 📦 Features

- ✅ Accepts a CSV file with `Query, Full Name, Username, Profile URL`
- 🔍 Searches:
  - Repository **name + description**
  - **Code files** using GitHub's code search
- 🧠 Prompts you interactively for keywords
- 🧾 Outputs matches to `user_matches.csv` including:
  - Full name
  - GitHub username
  - Profile URL
  - 📎 Link to the matched repository or file

---

## ⚙️ Requirements

- Python 3
- `pandas` and `requests` libraries

Install dependencies:

```bash
pip install pandas requests
```

---

## 🚀 Usage

```bash
python usersearch.py users.csv
```

You’ll be prompted like:

```text
Enter keywords to search (comma-separated): machine learning, flask, etl
```

---

## 📄 Input CSV Format

Your CSV should include at least the following columns:

```csv
Query,Full Name,Username,Profile URL
data science,Alice Johnson,alicejohnson,https://github.com/alicejohnson
etl,Bob Smith,bsmith,https://github.com/bsmith
```

> Column headers are **case-insensitive** and can contain spaces.

---

## 📤 Output Example (`user_matches.csv`)

```csv
fullname,username,profile_url,matched_url
Alice Johnson,alicejohnson,https://github.com/alicejohnson,https://github.com/alicejohnson/data-pipeline
```

---

## 🔐 GitHub API Token (Optional but Recommended)

To avoid hitting GitHub’s anonymous rate limits, add your personal access token inside the script:

```python
GITHUB_TOKEN = 'your_token_here'
```

Or load it from an environment variable:

```python
import os
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
```

---

## 🛠️ Customization Ideas

- Save `matched_keyword` as well
- Export to JSON instead of CSV
- Add CLI flags for keyword input or output name

---

## 🧠 Author & License

Built with 💻 by [gray-area]. MIT Licensed.

