#!/usr/bin/env python3
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "data" / "candidates.json"
RECORDS_PATH = ROOT / "data" / "records.json"
README_PATH = ROOT / "README.md"

TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"

def request_json(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-world-records",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8")), dict(resp.headers)

def safe_json(url):
    try:
        return request_json(url)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"warning: {url}: {exc}", file=sys.stderr)
        return None, {}

def repo_search(sort):
    q = quote("stars:>0" if sort == "stars" else "forks:>0")
    data, _ = safe_json(f"{API}/search/repositories?q={q}&sort={sort}&order=desc&per_page=1")
    if not data or not data.get("items"):
        return None
    item = data["items"][0]
    metric = "stargazers_count" if sort == "stars" else "forks_count"
    return {
        "category": "most_starred_repository" if sort == "stars" else "most_forked_repository",
        "holder": item["full_name"],
        "value": item[metric],
        "url": item["html_url"],
        "method": "global-search",
        "source": f"GitHub Search API sorted by {sort}",
    }

def user_search(sort, query):
    q = quote(query)
    data, _ = safe_json(f"{API}/search/users?q={q}&sort={sort}&order=desc&per_page=1")
    if not data or not data.get("items"):
        return None
    login = data["items"][0]["login"]
    details, _ = safe_json(f"{API}/users/{quote(login)}")
    if not details:
        return None
    if sort == "followers":
        category, value = "most_followed_user", details.get("followers")
    else:
        category, value = "most_public_repositories", details.get("public_repos")
    return {
        "category": category,
        "holder": login,
        "value": value,
        "url": details.get("html_url", f"https://github.com/{login}"),
        "method": "global-search",
        "source": f"GitHub Search API sorted by {sort} + User API verification",
    }

def user_following(login):
    data, _ = safe_json(f"{API}/users/{quote(login)}")
    if not data:
        return None
    return {
        "category": "most_following",
        "holder": login,
        "value": data.get("following"),
        "url": data.get("html_url", f"https://github.com/{login}"),
        "method": "candidate-based",
        "source": "GitHub User API",
    }

def parse_last_page(link_header):
    if not link_header:
        return None
    for part in link_header.split(","):
        if 'rel="last"' in part:
            m = re.search(r"[?&]page=(\d+)", part)
            if m:
                return int(m.group(1))
    return None

def commit_count(full_name):
    data, headers = safe_json(f"{API}/repos/{full_name}/commits?per_page=1")
    if not data:
        return None
    last = parse_last_page(headers.get("Link") or headers.get("link"))
    if last is not None:
        return last
    if isinstance(data, list):
        return len(data)
    return None

def best_candidate(category, candidates):
    best = None
    for candidate in candidates:
        if "/" in candidate:
            value = commit_count(candidate)
            url = f"https://github.com/{candidate}"
            source = "GitHub Commits API pagination"
        else:
            row = user_following(candidate)
            if not row:
                continue
            value = row["value"]
            url = row["url"]
            source = row["source"]
        if value is None:
            continue
        row = {
            "category": category,
            "holder": candidate,
            "value": value,
            "url": url,
            "method": "candidate-based",
            "source": source,
        }
        if best is None or row["value"] > best["value"]:
            best = row
    return best

def fmt_value(v):
    return f"{v:,}" if isinstance(v, int) else str(v)

def render_table(records, generated_at):
    labels = {
        "most_starred_repository": "Most starred repository",
        "most_forked_repository": "Most forked repository",
        "most_followed_user": "Most followed user",
        "most_public_repositories": "Most public repositories",
        "most_following": "Most following",
        "most_commits_any": "Most commits — any repository",
        "most_commits_real": "Most commits — real project",
    }
    lines = [
        f"_Last automated verification: **{generated_at}**_",
        "",
        "| Record | Holder | Value | Method |",
        "|---|---|---:|---|",
    ]
    for r in records:
        label = labels.get(r["category"], r["category"])
        holder = f"[\`{r['holder']}\`]({r['url']})"
        lines.append(f"| {label} | {holder} | **{fmt_value(r['value'])}** | \`{r['method']}\` |")
    return "\n".join(lines)

def update_readme(table):
    text = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r"<!-- RECORDS:START -->.*?<!-- RECORDS:END -->", re.S)
    replacement = f"<!-- RECORDS:START -->\n{table}\n<!-- RECORDS:END -->"
    if not pattern.search(text):
        raise RuntimeError("README record markers not found")
    README_PATH.write_text(pattern.sub(replacement, text), encoding="utf-8")

def main():
    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    records = []

    for row in [
        repo_search("stars"),
        repo_search("forks"),
        user_search("followers", "followers:>0 type:user"),
        user_search("repositories", "repos:>0 type:user"),
        best_candidate("most_following", candidates.get("most_following", [])),
        best_candidate("most_commits_any", candidates.get("most_commits_any", [])),
        best_candidate("most_commits_real", candidates.get("most_commits_real", [])),
    ]:
        if row and row.get("value") is not None:
            records.append(row)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "generated_at": now,
        "records": records,
        "notes": [
            "Global-search records are derived from GitHub Search API results.",
            "Candidate-based records are maxima only among data/candidates.json.",
            "Commit counts refer to commits reachable from the default branch where the API exposes pagination."
        ],
    }
    RECORDS_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    update_readme(render_table(records, now))
    print(f"updated {len(records)} records at {now}")

if __name__ == "__main__":
    main()
