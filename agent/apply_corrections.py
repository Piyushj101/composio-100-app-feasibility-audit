# -*- coding: utf-8 -*-
"""
Applies the 8 verification findings back onto the master dataset,
producing apps_final.json — the dataset actually shown on the case-study
page. Every row also gets `verified: true/false` so the page can show
exactly which rows were live-checked vs which still rest on reviewer
knowledge alone.
"""
import json

with open("/home/claude/composio_research/data/merged.json") as f:
    apps = json.load(f)

corrections = {
    "Pylon": dict(
        self_serve="yes",
        self_serve_note="VERIFIED: any Admin can generate a Bearer API token from Settings — no plan-gate found. Corrects an earlier low-confidence guess.",
        api_surface="VERIFIED broader than assumed: 22 documented resource groups (issues, accounts, contacts, KB, macros, surveys, custom objects...).",
        blocker="", buildability="yes", confidence="high", verified=True,
        evidence="docs.usepylon.com/pylon-docs/developer/api/authentication"),
    "Waterfall.io": dict(
        self_serve="yes",
        self_serve_note="VERIFIED: B2B contact/company data-enrichment API aggregating 30+ vendors. API key (x-api-key) issued on signup — fully self-serve. Corrects an earlier 'could not identify product' flag.",
        one_liner="B2B contact/company data enrichment API (30+ vendor aggregation).",
        api_surface="REST API, documented at docs.waterfall.io.",
        blocker="", buildability="yes", confidence="high", verified=True,
        evidence="docs.waterfall.io/v1/introduction"),
    "fanbasis": dict(
        self_serve="partial",
        self_serve_note="VERIFIED: fanbasis DOES have a documented payment/checkout API (API key, sandbox+prod, official npm SDK) — corrects an earlier 'no API found' claim. New finding: the docs portal itself (dev-docs.fanbasis.com) is password-gated, a merchant-approval-style blocker typical of payment platforms.",
        one_liner="Creator monetization / checkout platform (merchant-of-record payments API).",
        api_surface="REST checkout API + webhooks + official SDK, but docs require sign-in.",
        blocker="Developer docs portal is login-gated (merchant approval implied).",
        buildability="no", confidence="high", verified=True,
        evidence="github.com/otniel-bit/fbnewapi, dev-docs.fanbasis.com"),
    "Ahrefs": dict(
        self_serve="partial",
        self_serve_note="REFINED: still a hard paid-plan gate (no free tier), but 2026 sources show Ahrefs widened API v3 down to the Lite plan ($129/mo) — not Enterprise-exclusive as older sources (and the original pass-2 claim) suggested.",
        blocker="Paid-plan gate (from Lite tier up) — corrected from 'Enterprise-only'.",
        confidence="high", verified=True,
        evidence="trackseo.pro/blog/ahrefs-pricing, thatmarketingbuddy.com/pricing/ahrefs"),
    "LinkedIn Ads": dict(
        confidence="high", verified=True,
        self_serve_note="VERIFIED directly against LinkedIn/Microsoft's own docs: 'most permissions and partner programs require explicit approval.' Original finding confirmed unchanged.",
        evidence="learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access"),
    "Attio": dict(
        confidence="high", verified=True,
        self_serve_note="VERIFIED: API key (single workspace, self-serve) + OAuth2 (multi-workspace/public apps); official MCP server confirmed at attio.com/platform/developers.",
        evidence="docs.attio.com/rest-api/guides/authentication, attio.com/platform/developers"),
    "Otter.ai": dict(
        self_serve="partial",
        self_serve_note="CORRECTED: no public API existed through ~2024 (confirmed by third-party dev reports), but Otter.ai shipped a public enterprise/agent API in 2025 — Composio itself already lists an Otter.ai MCP toolkit. This is a real 'model knowledge was stale' catch.",
        api_surface="New (2025) enterprise-facing API for agent/CRM integrations; scope/openness not fully documented publicly.",
        buildability="yes", blocker="Enterprise-leaning rollout; self-serve breadth unclear.",
        mcp="yes (Otter.ai MCP exists, incl. via Composio)",
        confidence="medium", verified=True,
        evidence="itpro.com (Otter.ai third-party API launch, 2025), composio.dev/toolkits/otter_ai_mcp"),
    "Consensus": dict(
        confidence="high", verified=True,
        self_serve_note="VERIFIED and refined: request access at consensus.app/home/api, then use an x-api-key. Not instant, but not a sales-only gate either — a lightweight request form. Also has an MCP endpoint (mcp.goconsensus.com) sharing the same usage quota.",
        mcp="yes (mcp.goconsensus.com)",
        evidence="docs.consensus.app/api-get-started, help.consensus.app/en/articles/16516328-the-consensus-api"),
}

for a in apps:
    if a["app"] in corrections:
        a.update(corrections[a["app"]])
    else:
        a["verified"] = False

with open("/home/claude/composio_research/data/apps_final.json", "w") as f:
    json.dump(apps, f, indent=2)

verified_n = sum(1 for a in apps if a.get("verified"))
print(f"Applied corrections to {len(corrections)} rows. "
      f"{verified_n}/{len(apps)} rows now marked verified=true.")
