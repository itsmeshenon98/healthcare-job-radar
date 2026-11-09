# Healthcare Job Radar
GitHub-only healthcare job dashboard + scheduled public ATS ingestion.

## Enable GitHub Pages
Repository **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**.
Website: https://itsmeshenon98.github.io/healthcare-job-radar/

## Run ingestion
Actions → **Refresh healthcare job feed** → Run workflow. Scheduled daily at 08:55 India time.
Workflow updates data/jobs.json and commits changes. No external database needed.

## Add employer boards
Edit scripts/ingest.py and add verified Greenhouse board slugs to GREENHOUSE or Lever site slugs to LEVER. Only public feeds; honor source terms. Does not scrape LinkedIn login pages or bypass restrictions.

Dashboard supports search, India/remote filters, categories, posting-age, saved/applied in localStorage and saved-job export. Dataset starts empty until ingestion completes.
