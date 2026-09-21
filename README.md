# GitHub World Records

> Tracking the biggest, oldest, fastest and strangest records on GitHub.

[![Update records](https://github.com/Berserk-hub150/github-world-records/actions/workflows/update-records.yml/badge.svg)](https://github.com/Berserk-hub150/github-world-records/actions/workflows/update-records.yml)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**GitHub World Records** is a community-maintained, reproducible collection of notable GitHub records.

This project is **not affiliated with GitHub or Guinness World Records**.

## Records

<!-- RECORDS:START -->
Run the `Update records` GitHub Action to populate live records.
<!-- RECORDS:END -->

## Record types

| Category | Discovery method |
|---|---|
| Most starred repository | GitHub Search API |
| Most forked repository | GitHub Search API |
| Most followed user | GitHub Search API + User API |
| Most public repositories | GitHub Search API + User API |
| Most following | Candidate-based verification |
| Most commits — any repository | Candidate-based verification |
| Most commits — real project | Candidate-based verification |

Some GitHub metrics can be globally sorted through the API. Others cannot. For those, this repository clearly labels the result as **candidate-based** instead of pretending it is a mathematically proven global maximum.

## Current seed records

Two commit records are included as initial verified candidates:

- `virejdasani/Commited` — **3,000,007 commits**. This is an intentionally generated record repository and is classified as **synthetic / record attempt**.
- `chromium/chromium` — a real software project with more than **1.8 million commits** on its GitHub mirror as of September 2026.

The updater re-checks candidates where GitHub's API allows a reliable count.

## Verification rules

A record must include:

1. A public GitHub URL.
2. A measurable value.
3. A source or reproducible API method.
4. A verification timestamp.
5. A classification such as `global-search`, `candidate-based`, or `manual`.
6. For unusual records, enough evidence for another person to reproduce the result.

No screenshots alone. No unverifiable claims.

## Submit a record

Found something bigger?

Open a **Record Claim** issue and provide the holder, value, GitHub URL, evidence, and verification method.

Pull requests that add better discovery methods are especially welcome.

## Automated updates

The workflow in `.github/workflows/update-records.yml` runs daily and can also be triggered manually.

It:

1. queries GitHub for globally sortable metrics;
2. checks curated candidates for non-sortable metrics;
3. writes `data/records.json`;
4. regenerates the Records table in this README;
5. commits changes only when values changed.

## Add candidates

Edit `data/candidates.json`.

```json
{
  "most_following": ["example-user"],
  "most_commits_any": ["virejdasani/Commited"],
  "most_commits_real": ["chromium/chromium"]
}
```

Candidate-based categories are intentionally transparent: a better candidate can replace the current holder as soon as it is verified.

## Roadmap

- More user records
- More repository records
- Contributor and issue/PR records
- Historical snapshots
- Record history / previous holders
- GitHub Pages leaderboard
- JSON API for other projects
- ClickHouse-based discovery for metrics unavailable in GitHub Search

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT.
