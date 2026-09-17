# -*- coding: utf-8 -*-
"""
PASS 1 — the actual automated research agent.

For every app in apps_master.json, this script:
  1. Fetches the hint URL over HTTP (real network call, real docs site).
  2. Records HTTP status / redirect chain / content length.
  3. Runs keyword heuristics over the fetched HTML to *guess*:
       - auth signals present (oauth, api key, bearer, basic auth, jwt)
       - api-shape signals (rest, graphql, webhook)
       - self-serve signals (sign up, free trial, get api key) vs
         gate signals (contact sales, request access, apply, partner program)
       - mcp signals ("model context protocol", "mcp server")
  4. Saves everything to pass1_results.json — with NO human correction.

This is deliberately dumb: it is meant to show what a naive scraping agent
gets right/wrong on its own, before any review. Many docs sites block
bots, gate content behind JS rendering, or redirect to marketing pages —
that failure mode is itself one of the findings.
"""
import json, re, time, socket
import urllib.request, urllib.error

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ComposioResearchAgent/1.0; +https://composio.dev)"
}

KEYWORDS = {
    "oauth":      [r"oauth\s*2", r"oauth2", r"authorization code", r"oauth"],
    "api_key":    [r"api[\s\-_]?key", r"access token", r"bearer token"],
    "basic_auth": [r"basic auth", r"http basic"],
    "jwt":        [r"\bjwt\b", r"json web token"],
    "graphql":    [r"graphql"],
    "rest":       [r"\brest api\b", r"restful"],
    "webhook":    [r"webhook"],
    "mcp":        [r"model context protocol", r"\bmcp server\b", r"\bmcp\b"],
    "self_serve": [r"sign up free", r"free trial", r"get (your |an )?api key",
                   r"start for free", r"create (a |an )?account", r"try (it )?free"],
    "gated":      [r"contact sales", r"request access", r"apply for access",
                   r"partner program", r"talk to sales", r"book a demo",
                   r"become a partner"],
}

def fetch(url, timeout=7):
    if not url.startswith("http"):
        url = "https://" + url
    req = urllib.request.Request(url, headers=HEADERS)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(400_000)  # cap payload
            status = resp.status
            final_url = resp.geturl()
        elapsed = round(time.time() - t0, 2)
        try:
            text = body.decode("utf-8", errors="ignore")
        except Exception:
            text = ""
        return {"ok": True, "status": status, "final_url": final_url,
                "bytes": len(body), "elapsed_s": elapsed, "text": text}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e), "elapsed_s": round(time.time()-t0,2)}
    except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
        return {"ok": False, "status": None, "error": str(e), "elapsed_s": round(time.time()-t0,2)}
    except Exception as e:
        return {"ok": False, "status": None, "error": f"{type(e).__name__}: {e}", "elapsed_s": round(time.time()-t0,2)}

def score_keywords(text):
    text_low = text.lower()
    hits = {}
    for label, patterns in KEYWORDS.items():
        found = any(re.search(p, text_low) for p in patterns)
        hits[label] = found
    return hits

def main():
    with open("/home/claude/composio_research/data/apps_master.json") as f:
        apps = json.load(f)

    results = []
    ok_count = 0
    for a in apps:
        r = fetch(a["url"])
        entry = {"id": a["id"], "app": a["app"], "url": a["url"]}
        entry.update({k: v for k, v in r.items() if k != "text"})
        if r.get("ok") and r.get("text"):
            entry["keyword_hits"] = score_keywords(r["text"])
            ok_count += 1
        else:
            entry["keyword_hits"] = None
        results.append(entry)
        print(f"[{a['id']:>3}] {a['app']:<28} ok={r.get('ok')} status={r.get('status')} "
              f"bytes={r.get('bytes','-')} t={r.get('elapsed_s')}s")

    with open("/home/claude/composio_research/data/pass1_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nFetch agent finished. {ok_count}/{len(apps)} URLs returned usable HTML "
          f"({round(100*ok_count/len(apps),1)}% success rate).")

if __name__ == "__main__":
    main()
