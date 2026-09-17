# Composio 100-App Feasibility Study — Research Agent

This repo is the actual
pipeline that produced the case-study page — not a mockup of one.

**Case study (live):** the published HTML page is the deliverable; see the
link shared alongside this repo.

## What's in here

```
agent/
  knowledge_base.py     # PASS 2 — reviewer/knowledge dataset for all 100 apps
                         #          (auth, self-serve, API surface, MCP, verdict,
                         #          confidence tag) — writes data/apps_master.json
  fetch_agent.py         # PASS 1 — the actual automated agent. Real HTTP GET
                         #          against every hint URL in the assignment,
                         #          keyword-heuristic scoring of the HTML.
                         #          Writes data/pass1_results.json
  analyze.py              # merges pass 1 + pass 2, computes the agent-vs-human
                         #          agreement rate, writes data/merged.json
  verification_log.py    # PASS 3 — 8 real web-search verification cases
                         #          (claim vs. what live search found vs. verdict)
                         #          writes data/verification.json
  apply_corrections.py   # applies the 8 verification findings back onto the
                         #          dataset -> data/apps_final.json (what the
                         #          page actually shows), marks verified=true/false
  final_analysis.py       # recomputes headline pattern stats + confidence
                         #          calibration -> data/patterns_final.json
  template.html          # the case-study page (design: Stitch "Technical Audit
                         #          Lab Notebook" system), with __APP_DATA__ /
                         #          __VERIF_DATA__ placeholders
  template_v1_legacy.html # earlier hand-styled version, kept for history
  stitch_design_reference.md # the original Stitch design-system spec (colors,
                         #          type scale, component rules) the current
                         #          template implements

data/
  apps_master.json       # pass 2 output (100 rows)
  pass1_results.json     # pass 1 output (100 rows, raw fetch + keyword hits)
  merged.json            # pass 1 + pass 2 merged
  verification.json      # 8 verification cases + summary
  apps_final.json        # FINAL dataset (what's embedded in the page)
  patterns_final.json    # headline pattern statistics

output/
  index.html             # the generated case-study page (apps_final.json +
                         #          verification.json embedded directly, so the
                         #          page computes and shows its own numbers
                         #          instead of hard-coded prose)
vercel.json              # static-deploy config (see "Deploying" below)
```

## How to run it end to end

```bash
cd agent
python3 knowledge_base.py        # -> data/apps_master.json          (pass 2)
python3 fetch_agent.py           # -> data/pass1_results.json        (pass 1, real network calls)
python3 analyze.py               # -> data/merged.json, data/patterns.json
python3 verification_log.py      # -> data/verification.json         (pass 3, hand-curated from real web searches)
python3 apply_corrections.py     # -> data/apps_final.json
python3 final_analysis.py        # -> data/patterns_final.json

# then, from the repo root, stitch data into the page template:
python3 - <<'PY'
import json
tmpl = open("agent/template.html", encoding="utf-8").read()
apps = json.load(open("data/apps_final.json"))
verif = json.load(open("data/verification.json"))
safe = lambda o: json.dumps(o).replace("</", "<\\/")
html = tmpl.replace("__APP_DATA__", safe(apps)).replace("__VERIF_DATA__", safe(verif))
open("output/index.html", "w", encoding="utf-8").write(html)
PY
```

`fetch_agent.py` makes 100 real outbound HTTP requests (one per app's hint
URL) — expect it to take roughly a minute and to log a handful of
403/404/timeout failures; that failure rate (94/100 succeeded in our run)
is itself one of the findings on the case-study page.

`verification_log.py` is **not** re-runnable as a live agent step in this
repo — the 8 cases in it are the actual search results I ran and read by
hand during this assignment, hand-transcribed with sources. Wiring pass 3
to a live search API (e.g. calling Composio's own SDK against a search
toolkit) is the natural next step and is called out explicitly on the case
study as "where a human was needed."

## Deploying

`output/index.html` is a single self-contained static file (Tailwind CDN +
Google Fonts, no build step, no server). Any static host works.

### Push to GitHub

```bash
cd composio_research
git init
git add .
git commit -m "Composio 100-app feasibility audit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

### Deploy on Vercel

Vercel needs to know the site root is `output/`. A `vercel.json` at the repo
root already does that:

```json
{
  "outputDirectory": "output"
}
```

Then either:
- **Dashboard**: vercel.com → "Add New Project" → import the GitHub repo you
  just pushed → it auto-detects `vercel.json` → Deploy.
- **CLI**: `npm i -g vercel`, then from the repo root: `vercel --prod`
  (first run will ask you to link/create a project — accept the defaults).

Either path gives you a public `https://<project>.vercel.app` URL. Every
subsequent `git push` to `main` auto-redeploys if you used the dashboard/Git
integration.

## Where Composio's own SDK/MCP would plug in

This was built inside an environment that already had first-class web
search and web-fetch tools available, which is what pass 1 and pass 3
actually used. The natural production version of this pipeline swaps:
- `fetch_agent.py`'s raw `urllib` calls for a Composio-orchestrated
  browser/fetch toolkit (so JS-rendered docs sites stop failing silently —
  6 of our 100 fetches failed for exactly this class of reason), and
- the hand-run verification searches in `verification_log.py` for an
  agent loop that calls a search MCP tool per low-confidence row and
  writes its own verification log automatically, instead of a human
  running 8 searches by hand.

## Honesty notes (see also the case-study page's "What Went Wrong" section)

- The dataset is a **reviewer's knowledge**, corrected by **8 real,
  cited web searches**, not 100 independently fact-checked rows. 11 of
  100 rows are still tagged `confidence: low` and unverified — they're
  visibly flagged as such in the table, not hidden.
- The raw agent (pass 1) is deliberately shown to be weak on its own
  (18.1% agreement with the reviewed verdict) — a naive keyword scraper
  is not sufficient, and the page says so rather than presenting pass 1
  as if it were the final answer.
- 2 of the 100 "apps" (Sherlock, Mermaid CLI) are open-source local
  tools with no hosted API/auth at all — they were kept in the dataset
  as an honest "not really buildable as an API toolkit" data point
  rather than dropped.
