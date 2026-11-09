# Healthcare Job Radar
GitHub-only healthcare startup job dashboard + scheduled public ATS ingestion.

## Automatic updates
- GitHub Actions runs every 6 hours (UTC).
- It fetches public job-board APIs, filters healthcare-relevant roles, deduplicates listings, and commits updates to `data/jobs.json`.
- GitHub Pages serves the dashboard and refreshed JSON; no database or server required.
- Workflow: Actions → **Refresh healthcare startup job feed**. Manual runs are also available.

## Enable GitHub Pages
Repository **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**.
Website: https://itsmeshenon98.github.io/healthcare-job-radar/

## Source coverage / caveat
Configured public ATS boards are listed in `scripts/ingest.py`; ingestion records per-board failures and successful source counts in `data/jobs.json`. The workflow reports source errors and fails if every configured source fails. This is not yet comprehensive startup discovery: adding a startup requires verifying its public ATS board token or another permitted feed. LinkedIn login-only listings are not scraped.

## Add employer boards
Confirm the company's public board token, then add it to `GREENHOUSE` or `LEVER` in `scripts/ingest.py`. Greenhouse public GET job-board endpoints are documented at https://docs.greenhouse.io/job-board.

Dashboard supports search, India/remote filters, categories, posting-age, saved/applied in localStorage and saved-job export.
