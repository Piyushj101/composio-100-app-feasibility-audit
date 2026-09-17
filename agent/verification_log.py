# -*- coding: utf-8 -*-
"""
PASS 3 — verification. Real web-search queries run against a sample of 8
apps (biased toward the lowest-confidence entries, plus two high-confidence
ones as control 'should-be-correct' checks). Each entry records the pass-2
claim, what the live search actually found, the verdict, and the source.
"""

VERIFICATION = [
    dict(app="Attio", pass2_confidence="medium",
         claim="OAuth2 + API key, self-serve, has an official MCP server.",
         found="Confirmed exactly: docs.attio.com describes both an API key "
               "(single workspace) and OAuth2 (for multi-workspace/public apps) "
               "under Bearer auth; attio.com/platform/developers confirms an "
               "official Attio MCP server.",
         verdict="HIT — pass-2 was correct, confidence upgraded to high.",
         source="docs.attio.com/rest-api/guides/authentication, attio.com/platform/developers"),

    dict(app="Pylon", pass2_confidence="low",
         claim="API key self-serve, but possibly gated behind a paid plan tier.",
         found="Corrected: any Admin user can generate a Bearer API token from "
               "Settings, no plan-gate mentioned in docs. Surface is much "
               "broader than assumed — 22 documented resource groups.",
         verdict="MISS (partially) — the 'paid-plan gate' guess was wrong; "
                 "self-serve status upgraded from 'partial' to 'yes'.",
         source="docs.usepylon.com/pylon-docs/developer/api/authentication, scalekit.com/blog/pylon-mcp-vs-api"),

    dict(app="Waterfall.io", pass2_confidence="low",
         claim="Could not confidently identify what this product is or whether it has an API.",
         found="Corrected: it's a B2B contact/company data-enrichment API "
               "(aggregates 30+ data vendors). Simple self-serve API key "
               "(x-api-key header) issued on signup. docs.waterfall.io is a "
               "real, live developer docs site.",
         verdict="MISS (was 'unknown') — fully resolved by search; "
                 "self-serve status upgraded from 'unknown' to 'yes'.",
         source="docs.waterfall.io/v1/introduction, waterfall.io"),

    dict(app="fanbasis", pass2_confidence="low",
         claim="No discoverable public API surface found.",
         found="Corrected: fanbasis DOES have a documented payment/checkout "
               "API (API-key auth, sandbox + production envs, an official "
               "npm SDK '@fanbasis/checkout-sdk', 13 webhook event types). "
               "However dev-docs.fanbasis.com itself is password-gated "
               "('Sign in to access API Docs') — a real, if different, gate.",
         verdict="MISS — the product does have an API; the actual finding "
                 "is 'docs require a login', not 'no API exists'.",
         source="github.com/otniel-bit/fbnewapi, dev-docs.fanbasis.com, npmjs.com/package/@fanbasis/checkout-sdk"),

    dict(app="Ahrefs", pass2_confidence="medium",
         claim="API v3 is gated to the Enterprise-tier plan only.",
         found="Partially corrected: multiple 2026 sources say Ahrefs widened "
               "API v3 access down to the Lite plan ($129/mo) in early 2026 "
               "(older articles describing 'Enterprise-only' are describing "
               "the deprecated v2 API or are now stale). It is still fully "
               "paid-plan-gated (no free tier), just not Enterprise-exclusive.",
         verdict="PARTIAL MISS — direction was right (paid-plan gate), "
                 "specific tier claim was outdated/wrong.",
         source="trackseo.pro/blog/ahrefs-pricing, blog.contentforce.ai/ahrefs-pricing, thatmarketingbuddy.com/pricing/ahrefs"),

    dict(app="LinkedIn Ads", pass2_confidence="high",
         claim="Not self-serve — requires LinkedIn Marketing Developer "
               "Platform partner-program approval before any real access.",
         found="Confirmed directly from Microsoft/LinkedIn's own developer "
               "docs: 'Most permissions and partner programs require "
               "explicit approval... Open Permissions are the only "
               "permissions available to all developers without approval.' "
               "Marketing/Ads access requires the partner program.",
         verdict="HIT — pass-2 was correct.",
         source="learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access"),

    dict(app="Otter.ai", pass2_confidence="low",
         claim="No public self-serve developer API found.",
         found="Corrected: true historically (through ~2024, third-party "
               "articles confirm 'Otter does not have an official API'), but "
               "Otter.ai announced a new public API for enterprise/agent "
               "integrations in 2025. Composio itself already lists an "
               "'Otter.ai MCP' toolkit — meaning it is now a live buildability "
               "candidate, not a dead end.",
         verdict="MISS — training-era knowledge was stale; the product shipped "
                 "an API after the knowledge cutoff. This is exactly the class "
                 "of error a live-search verification pass catches.",
         source="itpro.com/technology/artificial-intelligence/otter-ai-wants-to-bring-agents-to-third-party-systems, composio.dev/toolkits/otter_ai_mcp"),

    dict(app="Consensus", pass2_confidence="medium",
         claim="'OAuth requested' — apply-for-access gate, not instant self-serve.",
         found="Confirmed and refined: you request access at "
               "consensus.app/home/api, then get an x-api-key style key "
               "(current v1) — API access is a request/approval step, not "
               "instant, and it's bundled with a separate MCP endpoint "
               "(mcp.goconsensus.com) sharing the same call quota.",
         verdict="HIT — pass-2 was correct, plus new detail found (MCP exists, "
                 "shared usage pool).",
         source="docs.consensus.app/api-get-started, help.consensus.app/en/articles/16516328-the-consensus-api"),
]

if __name__ == "__main__":
    import json
    hits = sum(1 for v in VERIFICATION if v["verdict"].startswith("HIT"))
    misses = sum(1 for v in VERIFICATION if v["verdict"].startswith("MISS"))
    partial = sum(1 for v in VERIFICATION if "PARTIAL" in v["verdict"])
    n = len(VERIFICATION)
    summary = {
        "sample_size": n,
        "hits": hits,
        "misses": misses,
        "partial_misses": partial,
        "raw_pass2_accuracy_on_sample_pct": round(100 * hits / n, 1),
    }
    with open("/home/claude/composio_research/data/verification.json", "w") as f:
        json.dump({"cases": VERIFICATION, "summary": summary}, f, indent=2)
    print(json.dumps(summary, indent=2))
