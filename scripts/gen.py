"""Generate self-hosted profile cards (no third-party services needed)."""
import json, os, sys, math, html, datetime as dt, urllib.request

USER = "nimanazari"
TOKEN = os.environ["GITHUB_TOKEN"]
BG, BORDER, TITLE, TEXT, ACC, ACC2, MUTED = "#0d1117", "#1f2430", "#a78bfa", "#c9d1d9", "#8b5cf6", "#f472b6", "#8b949e"
FONT = "font-family='Segoe UI,Ubuntu,Helvetica,Arial,sans-serif'"

Q = """
query($u:String!){ user(login:$u){
  name login createdAt followers{totalCount}
  pullRequests{totalCount} issues{totalCount}
  repositoriesContributedTo(contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){totalCount}
  contributionsCollection{ totalCommitContributions restrictedContributionsCount
    contributionCalendar{ totalContributions weeks{ contributionDays{ contributionCount date } } } }
  repositories(first:100, ownerAffiliations:OWNER, orderBy:{field:UPDATED_AT,direction:DESC}){ totalCount nodes{
    name description stargazerCount forkCount isFork
    primaryLanguage{name color}
    languages(first:10, orderBy:{field:SIZE,direction:DESC}){ edges{ size node{name color} } } } }
}}"""


def gql(q, v):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": v}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    d = json.load(urllib.request.urlopen(req))
    if "errors" in d:
        print(d["errors"], file=sys.stderr)
    return d["data"]["user"]


def card(w, h, title, body):
    t = f'<text x="24" y="34" class="t a">{html.escape(title)}</text>' if title else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" {FONT}>
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC2}"/></linearGradient>
<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACC}" stop-opacity=".45"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient>
<style>.t{{font-size:18px;font-weight:700;fill:{TITLE}}}.l{{font-size:14px;fill:{TEXT}}}.b{{font-size:14px;font-weight:700;fill:{TEXT}}}.m{{font-size:12px;fill:{MUTED}}}
@keyframes fi{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}.a{{animation:fi .6s ease both}}</style></defs>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
{t}
{body}</svg>"""


def ico(x, y, d, c=ACC):
    return f'<path transform="translate({x},{y}) scale(.9)" fill="{c}" d="{d}"/>'


STAR = "M8 .25a.75.75 0 01.67.42l1.88 3.8 4.2.61a.75.75 0 01.42 1.28l-3.04 2.97.72 4.18a.75.75 0 01-1.09.79L8 12.35l-3.76 1.98a.75.75 0 01-1.09-.8l.72-4.17L.83 6.36a.75.75 0 01.41-1.28l4.2-.61L7.33.67A.75.75 0 018 .25z"
COMMIT = "M10.5 7.75a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm1.43.75a4 4 0 01-7.86 0H.75a.75.75 0 010-1.5h3.32a4 4 0 017.86 0h3.32a.75.75 0 010 1.5h-3.32z"
PR = "M7.18 1.31a.75.75 0 011.28.53v2.4h1.5a2.75 2.75 0 012.75 2.75v3.03a2.25 2.25 0 11-1.5 0V6.99c0-.69-.56-1.25-1.25-1.25h-1.5v2.4a.75.75 0 01-1.28.53L4.31 5.8a.75.75 0 010-1.06l2.87-3.43zM3.25 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zM1 3.25a2.25 2.25 0 113 2.12v5.26a2.25 2.25 0 11-1.5 0V5.37A2.25 2.25 0 011 3.25z"
ISSUE = "M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm9 3a1 1 0 11-2 0 1 1 0 012 0zm-.25-6.25a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0v-3.5z"
REPO = "M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.71 1.7.75.75 0 01-1.08 1.04A2.5 2.5 0 012 11.5v-9zm10.5-1V9h-8c-.36 0-.7.07-1 .2V2.5a1 1 0 011-1h8z"
FORK = "M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.12a2.25 2.25 0 10-1.5 0v.88c0 .69.56 1.25 1.25 1.25h2.5v2.03a2.25 2.25 0 101.5 0V7.5h2.5c.69 0 1.25-.56 1.25-1.25v-.88a2.25 2.25 0 10-1.5 0v.88H5v-.88zM11 3.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM7.25 11.75a.75.75 0 111.5 0 .75.75 0 01-1.5 0z"


def stats(u):
    repos = [r for r in u["repositories"]["nodes"] if not r["isFork"]]
    stars = sum(r["stargazerCount"] for r in repos)
    cc = u["contributionsCollection"]
    commits = cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
    prs, issues = u["pullRequests"]["totalCount"], u["issues"]["totalCount"]
    rows = [
        (STAR, "Total Stars", stars),
        (COMMIT, "Total Commits (this year)", commits),
        (PR, "Pull Requests", prs),
        (ISSUE, "Issues", issues),
        (REPO, "Contributed to", u["repositoriesContributedTo"]["totalCount"]),
    ]
    score = min(100, stars * 2 + commits / 5 + prs * 3 + u["followers"]["totalCount"] * 2 + len(repos) * 3)
    grade = "S" if score >= 90 else "A+" if score >= 75 else "A" if score >= 55 else "B+" if score >= 40 else "B" if score >= 25 else "C"
    body = ""
    for i, (d, l, v) in enumerate(rows):
        y = 62 + i * 26
        body += (f'<g class="a" style="animation-delay:{i*.12}s">{ico(24, y-13, d)}'
                 f'<text x="52" y="{y}" class="l">{l}:</text><text x="300" y="{y}" class="b">{v}</text></g>')
    r = 40; c = 2 * math.pi * r; off = c * (1 - score / 100)
    body += (f'<g transform="translate(410,110)"><circle r="{r}" fill="none" stroke="{BORDER}" stroke-width="7"/>'
             f'<circle r="{r}" fill="none" stroke="url(#g)" stroke-width="7" stroke-linecap="round" '
             f'stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}" transform="rotate(-90)">'
             f'<animate attributeName="stroke-dashoffset" from="{c:.1f}" to="{off:.1f}" dur="1.2s" fill="freeze"/></circle>'
             f'<text text-anchor="middle" dy="9" font-size="26" font-weight="800" fill="{TEXT}">{grade}</text></g>')
    return card(495, 195, f"{u['name'] or u['login']}'s GitHub Stats", body)


def langs(u):
    tot, col = {}, {}
    for r in u["repositories"]["nodes"]:
        if r["isFork"]:
            continue
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            tot[n] = tot.get(n, 0) + e["size"]
            col[n] = e["node"]["color"] or ACC
    items = sorted(tot.items(), key=lambda x: -x[1])[:8]
    s = sum(v for _, v in items) or 1
    body = '<g class="a">'; x = 24.0
    for n, v in items:
        w = max(2, 447 * v / s)
        body += f'<rect x="{x:.1f}" y="52" width="{w:.1f}" height="9" fill="{col[n]}"/>'
        x += w
    body += '</g>'
    for i, (n, v) in enumerate(items):
        cx = 24 + (i % 2) * 225; cy = 90 + (i // 2) * 24
        body += (f'<g class="a" style="animation-delay:{i*.1}s"><circle cx="{cx+5}" cy="{cy-5}" r="5" fill="{col[n]}"/>'
                 f'<text x="{cx+18}" y="{cy}" class="l">{html.escape(n)} <tspan class="m">{100*v/s:.1f}%</tspan></text></g>')
    return card(495, 90 + ((len(items) + 1) // 2) * 24 + 10, "Most Used Languages", body)


def activity(u):
    days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]][-31:]
    W, H, L, R, T, B = 900, 300, 50, 20, 50, 40
    mx = max(1, max(d["contributionCount"] for d in days))
    pts = []
    for i, d in enumerate(days):
        x = L + i * (W - L - R) / (len(days) - 1)
        y = T + (H - T - B) * (1 - d["contributionCount"] / mx)
        pts.append((x, y))
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{pts[0][0]:.1f},{H-B} " + line + f" {pts[-1][0]:.1f},{H-B}"
    body = ""
    for k in range(5):
        y = T + k * (H - T - B) / 4
        body += (f'<line x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="{BORDER}"/>'
                 f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end" class="m">{round(mx*(1-k/4))}</text>')
    body += (f'<polygon points="{area}" fill="url(#ar)" class="a"/>'
             f'<polyline points="{line}" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" class="a"/>')
    for i, ((x, y), d) in enumerate(zip(pts, days)):
        body += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{ACC2}" class="a" style="animation-delay:{i*.02}s">'
                 f'<title>{d["date"]}: {d["contributionCount"]} contributions</title></circle>')
        if i % 5 == 0:
            body += f'<text x="{x:.1f}" y="{H-B+18}" text-anchor="middle" class="m">{d["date"][5:]}</text>'
    return card(W, H, "Contribution Graph (last 31 days)", body)


def trophies(u):
    repos = [r for r in u["repositories"]["nodes"] if not r["isFork"]]
    cc = u["contributionsCollection"]
    commits = cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
    years = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))).days // 365
    names = ["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"]

    def tier(v, th):
        return next((n for n, t in zip(names, th) if v >= t), "C")

    items = [
        ("Commits", commits, [2000, 1000, 500, 200, 100, 50, 10, 0]),
        ("Repositories", len(repos), [100, 50, 30, 20, 10, 5, 2, 0]),
        ("Stars", sum(r["stargazerCount"] for r in repos), [1000, 500, 200, 100, 50, 10, 1, 0]),
        ("Followers", u["followers"]["totalCount"], [1000, 500, 200, 100, 50, 10, 1, 0]),
        ("Pull Requests", u["pullRequests"]["totalCount"], [500, 200, 100, 50, 20, 10, 1, 0]),
        ("Issues", u["issues"]["totalCount"], [500, 200, 100, 50, 20, 10, 1, 0]),
        ("Experience", years, [10, 7, 5, 4, 3, 2, 1, 0]),
    ]
    tc = {"SSS": "#facc15", "SS": "#fb923c", "S": "#f472b6", "AAA": "#a78bfa", "AA": "#60a5fa", "A": "#34d399", "B": "#9ca3af", "C": "#6b7280"}
    body = ""
    for i, (n, v, th) in enumerate(items):
        t = tier(v, th); c = tc[t]; cx = 24 + i * 116 + 52; cy = 78
        hexp = " ".join(f"{cx + 40*math.cos(a):.1f},{cy + 40*math.sin(a):.1f}" for a in [math.pi / 6 * (2 * k + 1) for k in range(6)])
        body += (f'<g class="a" style="animation-delay:{i*.1}s"><polygon points="{hexp}" fill="{c}22" stroke="{c}" stroke-width="2"/>'
                 f'<text x="{cx}" y="{cy+8}" text-anchor="middle" font-size="20" font-weight="800" fill="{c}">{t}</text>'
                 f'<text x="{cx}" y="140" text-anchor="middle" class="b">{n}</text>'
                 f'<text x="{cx}" y="158" text-anchor="middle" class="m">{v}{" yrs" if n == "Experience" else ""}</text></g>')
    return card(24 + len(items) * 116 + 8, 175, "Trophies", body)


def pin(r):
    d = html.escape((r["description"] or "No description")[:70])
    pl = r["primaryLanguage"] or {"name": "Unknown", "color": MUTED}
    body = (f'{ico(24, 50, REPO)}<text x="52" y="62" class="b" fill="{TITLE}">{html.escape(r["name"])}</text>'
            f'<text x="24" y="92" class="l">{d}</text>'
            f'<g class="a"><circle cx="30" cy="125" r="6" fill="{pl["color"] or MUTED}"/><text x="42" y="130" class="l">{pl["name"]}</text>'
            f'{ico(150, 118, STAR, MUTED)}<text x="170" y="130" class="l">{r["stargazerCount"]}</text>'
            f'{ico(215, 118, FORK, MUTED)}<text x="235" y="130" class="l">{r["forkCount"]}</text></g>')
    return card(400, 150, "", body)


u = gql(Q, {"u": USER})
out = {"stats.svg": stats(u), "langs.svg": langs(u), "activity.svg": activity(u), "trophies.svg": trophies(u)}
for r in u["repositories"]["nodes"]:
    if r["name"] in ("smarthome-vacuumleague", "smarthome-teams"):
        out[f"pin-{r['name']}.svg"] = pin(r)
os.makedirs("assets", exist_ok=True)
for k, v in out.items():
    open(f"assets/{k}", "w", encoding="utf-8").write(v)
print("generated:", ", ".join(out))
