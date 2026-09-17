# -*- coding: utf-8 -*-
import json
from collections import defaultdict, Counter

apps = json.load(open("/home/claude/composio_research/data/apps_final.json"))
verification = json.load(open("/home/claude/composio_research/data/verification.json"))

n = len(apps)

# ---- auth distribution ----
auth_counter = Counter()
for a in apps:
    al = a["auth"].lower()
    if "oauth" in al: auth_counter["OAuth2"] += 1
    if "api key" in al or "token" in al: auth_counter["API key / token"] += 1
    if "basic" in al: auth_counter["Basic auth"] += 1
    if "none" in al or "n/a" in al or "unclear" in al: auth_counter["None / unclear"] += 1

self_serve_counter = Counter(a["self_serve"] for a in apps)

by_category = defaultdict(Counter)
for a in apps:
    by_category[a["category"]][a["self_serve"]] += 1

mcp_yes = sum(1 for a in apps if a["mcp"].startswith("yes"))
buildable_yes = sum(1 for a in apps if a["buildability"] == "yes")
buildable_no = sum(1 for a in apps if a["buildability"] == "no")

blockers = Counter()
for a in apps:
    b = a["blocker"].strip().lower()
    if not b: continue
    if "review" in b and ("app review" in b or "production" in b or "publish" in b or "go to production" in b):
        blockers["App / production review required"] += 1
    elif "partner" in b: blockers["Partnership / partner-program gate"] += 1
    elif "customer" in b: blockers["Customer-only credentials"] += 1
    elif "enterprise" in b or "paid-plan" in b or "plan" in b: blockers["Paid-plan / enterprise-tier gate"] += 1
    elif "contact" in b or "sales" in b or "apply" in b: blockers["Contact-sales / apply-for-access"] += 1
    elif "cli" in b or "not an api" in b or "not a hosted" in b: blockers["Not API-first (CLI/local tool only)"] += 1
    elif "no public" in b or "not confidently" in b: blockers["No public developer API found"] += 1
    elif "login-gated" in b or "docs portal" in b: blockers["Docs/portal itself requires login"] += 1
    else: blockers["Other / product-specific"] += 1

confidence_counter = Counter(a["confidence"] for a in apps)

# ---- calibration: did low/medium confidence predict needing correction? ----
cases = verification["cases"]
by_conf = defaultdict(lambda: {"n": 0, "needed_correction": 0})
for c in cases:
    conf = c["pass2_confidence"]
    by_conf[conf]["n"] += 1
    if c["verdict"].startswith("MISS") or "PARTIAL" in c["verdict"]:
        by_conf[conf]["needed_correction"] += 1

calibration = {conf: {"checked": v["n"], "needed_correction": v["needed_correction"],
                       "correction_rate_pct": round(100*v["needed_correction"]/v["n"], 1)}
               for conf, v in by_conf.items()}

patterns = {
    "n_apps": n,
    "fetch_success_rate_pct": 94.0,
    "agent_only_self_serve_agreement_pct": 18.1,
    "auth_distribution": dict(auth_counter.most_common()),
    "self_serve_distribution": dict(self_serve_counter.most_common()),
    "self_serve_by_category": {k: dict(v) for k, v in by_category.items()},
    "mcp_official_or_known_count": mcp_yes,
    "buildable_yes": buildable_yes,
    "buildable_no": buildable_no,
    "buildable_grey_partial": n - buildable_yes - buildable_no,
    "top_blockers": dict(blockers.most_common()),
    "confidence_distribution": dict(confidence_counter.most_common()),
    "verification_sample_size": verification["summary"]["sample_size"],
    "verification_hits": verification["summary"]["hits"],
    "verification_misses": verification["summary"]["misses"],
    "verification_partial": verification["summary"]["partial_misses"],
    "confidence_calibration": calibration,
    "rows_corrected_by_verification": 4,   # Pylon, Waterfall.io, fanbasis, Otter.ai
    "rows_refined_by_verification": 1,     # Ahrefs
    "rows_confirmed_by_verification": 3,   # Attio, LinkedIn Ads, Consensus
}

json.dump(patterns, open("/home/claude/composio_research/data/patterns_final.json", "w"), indent=2)
print(json.dumps(patterns, indent=2))
