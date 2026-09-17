# -*- coding: utf-8 -*-
"""
Merges PASS 1 (agent fetch+keyword heuristics) with PASS 2 (knowledge-base
review) into one merged dataset, flags where the naive agent's raw keyword
signal agreed/disagreed with the reviewed conclusion, and computes the
headline pattern statistics used on the case-study page.
"""
import json
from collections import defaultdict, Counter

with open("/home/claude/composio_research/data/apps_master.json") as f:
    apps = json.load(f)
with open("/home/claude/composio_research/data/pass1_results.json") as f:
    pass1 = {r["id"]: r for r in json.load(f)}

merged = []
agent_agree = 0
agent_checked = 0

for a in apps:
    p1 = pass1.get(a["id"], {})
    hits = p1.get("keyword_hits")
    fetch_ok = p1.get("ok", False)

    agent_self_serve_guess = None
    agent_note = None
    if hits:
        agent_checked += 1
        # crude agent verdict: gated keywords beat self-serve keywords
        if hits.get("gated") and not hits.get("self_serve"):
            agent_self_serve_guess = "no"
        elif hits.get("self_serve") and not hits.get("gated"):
            agent_self_serve_guess = "yes"
        elif hits.get("self_serve") and hits.get("gated"):
            agent_self_serve_guess = "partial"
        else:
            agent_self_serve_guess = "unclear"

        human_bucket = a["self_serve"]
        human_bucket_norm = "yes" if human_bucket == "yes" else (
            "no" if human_bucket in ("no",) else "partial")
        if agent_self_serve_guess in ("unclear",):
            pass  # not counted as agree/disagree, agent had no signal
        else:
            agent_agree += int(agent_self_serve_guess == human_bucket_norm)
    else:
        agent_note = "fetch failed — agent had zero signal, pure human/knowledge fallback"

    row = dict(a)
    row["fetch_ok"] = fetch_ok
    row["fetch_status"] = p1.get("status")
    row["agent_keyword_hits"] = hits
    row["agent_self_serve_guess"] = agent_self_serve_guess
    row["agent_note"] = agent_note
    merged.append(row)

with open("/home/claude/composio_research/data/merged.json", "w") as f:
    json.dump(merged, f, indent=2)

# ---------------- pattern computation ----------------
n = len(merged)
auth_counter = Counter()
for a in merged:
    auth_low = a["auth"].lower()
    if "oauth" in auth_low:
        auth_counter["OAuth2"] += 1
    if "api key" in auth_low or "token" in auth_low:
        auth_counter["API key / token"] += 1
    if "basic" in auth_low:
        auth_counter["Basic auth"] += 1
    if "none" in auth_low or "n/a" in auth_low or "unclear" in auth_low:
        auth_counter["None / unclear (not a hosted API)"] += 1

self_serve_counter = Counter(a["self_serve"] for a in merged)

by_category = defaultdict(lambda: Counter())
for a in merged:
    by_category[a["category"]][a["self_serve"]] += 1

mcp_yes = sum(1 for a in merged if a["mcp"].startswith("yes"))
buildable_yes = sum(1 for a in merged if a["buildability"] == "yes")
buildable_no = sum(1 for a in merged if a["buildability"] == "no")

blockers = Counter()
for a in merged:
    b = a["blocker"].strip()
    if not b:
        continue
    bl = b.lower()
    if "review" in bl and ("app review" in bl or "production" in bl or "publish" in bl):
        blockers["App/production review required"] += 1
    elif "partner" in bl or "partnership" in bl:
        blockers["Partnership / partner-program gate"] += 1
    elif "customer" in bl or "existing customer" in bl:
        blockers["Customer-only credentials (must already be a paying user)"] += 1
    elif "enterprise" in bl or "paid" in bl or "plan" in bl:
        blockers["Paid-plan / enterprise-tier gate"] += 1
    elif "contact" in bl or "sales" in bl or "apply" in bl:
        blockers["Contact-sales / apply-for-access gate"] += 1
    elif "not an api" in bl or "cli" in bl.lower() or "not a hosted" in bl:
        blockers["Not API-first (CLI tool / no hosted service)"] += 1
    elif "no public" in bl or "no discoverable" in bl or "not confidently" in bl:
        blockers["No public developer API found"] += 1
    else:
        blockers["Other / product-specific friction"] += 1

confidence_counter = Counter(a["confidence"] for a in merged)

patterns = {
    "n_apps": n,
    "fetch_success_rate": round(100 * sum(1 for a in merged if a["fetch_ok"]) / n, 1),
    "auth_distribution": dict(auth_counter.most_common()),
    "self_serve_distribution": dict(self_serve_counter.most_common()),
    "self_serve_by_category": {k: dict(v) for k, v in by_category.items()},
    "mcp_official_count": mcp_yes,
    "buildable_yes": buildable_yes,
    "buildable_no": buildable_no,
    "buildable_partial_or_yes_with_blocker": n - buildable_yes - buildable_no,
    "top_blockers": dict(blockers.most_common()),
    "reviewer_confidence_distribution": dict(confidence_counter.most_common()),
    "agent_only_agreement_pct": round(100 * agent_agree / agent_checked, 1) if agent_checked else None,
    "agent_checked_n": agent_checked,
}

with open("/home/claude/composio_research/data/patterns.json", "w") as f:
    json.dump(patterns, f, indent=2)

print(json.dumps(patterns, indent=2))
