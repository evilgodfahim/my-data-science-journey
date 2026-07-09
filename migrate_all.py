#!/usr/bin/env python3
import base64, os, re, sys, time
import requests
from nacl import encoding, public

TOKEN        = os.environ["GITHUB_TOKEN"]
OWNER        = "evilgodfahim"
SECRET_NAME  = "WEBSHARE_PROXY_URL"
SECRET_VALUE = os.environ.get("WEBSHARE_PROXY_URL", "")
DRY_RUN      = "--apply" not in sys.argv

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

IMAGE_RE = re.compile(r'ghcr\.io/thephaseless/byparr:[^\s\'"]+', re.IGNORECASE)
SKIP_EXTENSIONS = {'.md', '.txt', '.rst', '.mdx'}

def log(msg):
    print(msg, flush=True)

def github_request(method, url, **kwargs):
    """Wrapper to safely handle network drops, timeouts, and GitHub rate limits."""
    timeout = kwargs.pop("timeout", 30)
    headers = kwargs.pop("headers", HEADERS)
    retries = 3
    
    while retries > 0:
        try:
            r = requests.request(method, url, timeout=timeout, headers=headers, **kwargs)
            if r.status_code in (403, 429) and "X-RateLimit-Reset" in r.headers:
                reset_time = int(r.headers.get("X-RateLimit-Reset", time.time() + 60))
                wait = max(reset_time - time.time(), 5)
                log(f"  [API Limit] Rate limit hit. Waiting {wait:.0f}s before continuing...")
                time.sleep(wait)
                continue
            
            r.raise_for_status()
            return r
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            retries -= 1
            if retries == 0:
                raise e
            log(f"  [Network Issue] Retrying in 5s... ({str(e)})")
            time.sleep(5)

def trawl_steps(indent):
    i = indent
    return (
        f"{i}- name: Start Redis\n"
        f"{i}  run: |\n"
        f"{i}    docker network create trawl-net\n"
        f"{i}    docker run -d \\\n"
        f"{i}      --name redis \\\n"
        f"{i}      --network trawl-net \\\n"
        f"{i}      redis:alpine\n"
        "\n"
        f"{i}- name: Start Trawl\n"
        f"{i}  run: |\n"
        f"{i}    docker run -d \\\n"
        f"{i}      --name trawl \\\n"
        f"{i}      --network trawl-net \\\n"
        f"{i}      -p 8191:8191 \\\n"
        f"{i}      -e REDIS_URL=redis://redis:6379 \\\n"
        f"{i}      -e BROWSER_POOL_SIZE=2 \\\n"
        f"{i}      -e RESIDENTIAL_PROXY_URL=${{{{ secrets.WEBSHARE_PROXY_URL }}}} \\\n"
        f"{i}      ghcr.io/germondai/trawl:latest\n"
        "\n"
        f"{i}- name: Wait for Trawl\n"
        f"{i}  run: |\n"
        f"{i}    for i in $(seq 1 40); do\n"
        f"{i}      curl -sf http://localhost:8191/health && echo 'Trawl ready' && exit 0\n"
        f"{i}      sleep 2\n"
        f"{i}    done\n"
        f"{i}    docker logs trawl && exit 1"
    )

def patch_workflow(content):
    # FIXED: Replaced unsafe regex with a fast, linear string parser for the services block
    in_services = False
    for line in content.splitlines():
        if line.strip().startswith('services:'):
            in_services = True
        elif in_services and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
            in_services = False
        if in_services and 'byparr:' in line:
            log("    ⚠  Contains a 'services:' block — needs manual conversion")
            break

    lines = content.split('\n')
    result = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s+)-\s+name:', line)
        if m:
            indent = m.group(1)
            step_lines = [line]
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if nxt and re.match(rf'^{re.escape(indent)}-\s', nxt):
                    break
                step_lines.append(nxt)
                j += 1
            step_text = '\n'.join(step_lines)
            if IMAGE_RE.search(step_text):
                result.append(trawl_steps(indent))
                changed = True
                if j < len(lines) and re.match(rf'^{re.escape(indent)}-\s+name:', lines[j]):
                    peek, k = [], j
                    while k < len(lines):
                        nxt = lines[k]
                        if k > j and nxt and re.match(rf'^{re.escape(indent)}-\s', nxt):
                            break
                        peek.append(nxt)
                        k += 1
                    peek_text = '\n'.join(peek)
                    # FIXED: Replaced generic \s with explicit horizontal spacing [ \t] and explicit line breaks to eliminate backtracking hangs
                    if (re.search(r'run:[ \t]*\|?[ \t]*\n(?:[ \t]*\r?\n)*[ \t]*sleep[ \t]+\d+', peek_text, re.IGNORECASE)
                            and not re.search(r'docker|python|pip|git|curl|npm|node|wget', peek_text, re.IGNORECASE)):
                        j = k
                i = j
                continue
        if 'byparr' in line.lower():
            new_line = IMAGE_RE.sub('ghcr.io/germondai/trawl:latest', line)
            new_line = re.sub(r'--name\s+byparr\b', '--name trawl', new_line)
            new_line = new_line.replace('docker logs byparr', 'docker logs trawl')
            if new_line != line:
                line = new_line
                changed = True
        result.append(line)
        i += 1
    return '\n'.join(result), changed

def patch_compose(content):
    new = IMAGE_RE.sub('ghcr.io/germondai/trawl:latest', content)
    new = re.sub(r'(container_name:\s*)byparr', r'\1trawl', new)
    new = re.sub(r'^(\s*)byparr(\s*:)', r'\1trawl\2', new, flags=re.MULTILINE)
    new = re.sub(r'--name\s+byparr\b', '--name trawl', new)
    if new != content:
        log("    ⚠  docker-compose: updated but Redis must be added manually")
    return new, new != content

def patch_other(content):
    new = IMAGE_RE.sub('ghcr.io/germondai/trawl:latest', content)
    new = re.sub(r'--name\s+byparr\b', '--name trawl', new)
    new = new.replace('docker logs byparr', 'docker logs trawl')
    return new, new != content

def patch(content, path):
    name = path.lower()
    if 'compose' in name:
        return patch_compose(content)
    if name.endswith(('.yml', '.yaml')):
        return patch_workflow(content)
    return patch_other(content)

def get_all_repos():
    repos, page = [], 1
    while True:
        log(f"  Fetching repo list page {page}...")
        r = github_request("GET", "https://api.github.com/user/repos", params={"per_page": 100, "page": page, "type": "owner"})
        batch = r.json()
        if not batch:
            break
        repos.extend(b["name"] for b in batch)
        page += 1
    return repos

def search_files():
    results, page = [], 1
    while True:
        log(f"  Searching page {page}...")
        r = github_request("GET", "https://api.github.com/search/code", params={"q": f"byparr user:{OWNER}", "per_page": 100, "page": page})
        batch = r.json().get("items", [])
        results.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        time.sleep(2)
    return results

def get_file(repo, path):
    log(f"    → reading {repo}/{path}")
    r = github_request("GET", f"https://api.github.com/repos/{OWNER}/{repo}/contents/{path}")
    return r.json()

def put_file(repo, path, content, sha):
    log(f"    → writing {repo}/{path}")
    github_request("PUT", f"https://api.github.com/repos/{OWNER}/{repo}/contents/{path}", json={
        "message": "chore: replace Byparr with Trawl",
        "content": base64.b64encode(content.encode()).decode(),
        "sha": sha,
    })

def encrypt_secret(public_key_b64, secret):
    pk  = public.PublicKey(public_key_b64.encode(), encoding.Base64Encoder())
    box = public.SealedBox(pk)
    return base64.b64encode(box.encrypt(secret.encode())).decode()

def set_secret(repo):
    log(f"  → getting public key for {repo}")
    r = github_request("GET", f"https://api.github.com/repos/{OWNER}/{repo}/actions/secrets/public-key")
    key_data = r.json()
    encrypted = encrypt_secret(key_data["key"], SECRET_VALUE)
    
    log(f"  → setting secret for {repo}")
    github_request("PUT", f"https://api.github.com/repos/{OWNER}/{repo}/actions/secrets/{SECRET_NAME}", json={
        "encrypted_value": encrypted, 
        "key_id": key_data["key_id"]
    })

# ── Main ──────────────────────────────────────────────────────────────────────

log(f"{'[DRY RUN] ' if DRY_RUN else ''}Starting...\n")

log("── STEP 1: Byparr → Trawl ────────────────────────────────────────────")
items = search_files()
log(f"Found {len(items)} file(s)\n")

updated, skipped, failed = [], [], []
seen = set()

for item in items:
    repo = item["repository"]["name"]
    path = item["path"]
    key  = f"{repo}/{path}"

    if any(path.lower().endswith(ext) for ext in SKIP_EXTENSIONS):
        log(f"  [SKIP] {key}  (doc file)")
        continue

    # FIXED: Skip the migration script file itself to protect runtime integrity
    if "migrate_all.py" in path.lower():
        log(f"  [SKIP] {key}  (migration script self-exclusion)")
        continue

    if key in seen:
        continue
    seen.add(key)

    try:
        data        = get_file(repo, path)
        content     = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        new_content, changed = patch(content, path)

        if not changed:
            log(f"  [~] {key}  (no patchable reference)")
            skipped.append(key)
        else:
            if DRY_RUN:
                log(f"  [WOULD CHANGE] {key}")
            else:
                put_file(repo, path, new_content, data["sha"])
                log(f"  [✓] {key}")
            updated.append(key)

        time.sleep(0.5)
    except Exception as e:
        log(f"  [✗] {key}: {e}")
        failed.append(key)
        time.sleep(1)

log(f"\nPatched: {len(updated)}  Skipped: {len(skipped)}  Failed: {len(failed)}")

log("\n── STEP 2: Set WEBSHARE_PROXY_URL in all repos ───────────────────────")
all_repos = get_all_repos()
log(f"Found {len(all_repos)} repos\n")

s_ok, s_fail = [], []

for repo in all_repos:
    try:
        if not DRY_RUN:
            set_secret(repo)
        log(f"  {'[WOULD SET]' if DRY_RUN else '[✓]'} {repo}")
        s_ok.append(repo)
    except Exception as e:
        log(f"   [✗] {repo}: {e}")
        s_fail.append(repo)
    time.sleep(0.3)

log(f"\nSecrets set: {len(s_ok)}  Failed: {len(s_fail)}")
log("\n══════════════════════════════════════════════════════════════════════")
log("Dry run done. Run with --apply to commit." if DRY_RUN else "All done.")