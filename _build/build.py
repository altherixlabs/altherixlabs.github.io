#!/usr/bin/env python3
"""Static site generator for altherix.in.
Run from the repo root:  python3 _build/build.py
Writes plain HTML files; GitHub Pages serves them as-is (Jekyll ignores _build/)."""
import json, os, re, subprocess, sys, datetime
from html import escape as E
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = []
V = "13"  # asset cache-buster

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

def url_for(path):
    return SITE + "/" + path.replace("index.html", "")

TODAY = datetime.date.today().isoformat()

def _git(*args):
    try:
        return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return None

def git_dates(rel):
    """(first, last) commit dates of a generated file, or (None, None) if it isn't committed yet."""
    r = _git("log", "--follow", "--format=%cs", "--", rel)
    dates = r.stdout.split() if r and r.returncode == 0 else []
    return (dates[-1], dates[0]) if dates else (None, None)

def committed_text(rel):
    r = _git("show", f"HEAD:{rel}")
    return r.stdout if r and r.returncode == 0 else None

def changed_since_commit(rel):
    """True if the file on disk differs from the last commit (or was never committed)."""
    old = committed_text(rel)
    if old is None:
        return True
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read() != old

def last_modified(rel):
    return TODAY if changed_since_commit(rel) else (git_dates(rel)[1] or TODAY)

def dot(items):
    # keep each separator attached to the item before it, so wrapped lines never start with "·"
    return "\u00a0· ".join(E(t).replace(" ", "\u00a0") if len(t) < 18 else E(t) for t in items)

# ── chrome ───────────────────────────────────────────────────────────────────
NAV = [("Services", "/#services", "services"), ("Solutions", "/#solutions", "solutions"),
       ("Case Studies", "/case-studies/", "case-studies"), ("Products", "/products/", "products"), ("What we build", "/#build", "industries"),
       ("About", "/#about", "about"), ("Careers", "/careers.html", "careers")]

def head(title, desc, path, jsonld=None, og_type="website", noindex=False, og_image="/assets/og.png", og_w=1200, og_h=630):
    u = url_for(path)
    ld = "".join(f'\n<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    canonical = "" if noindex else f'\n<link rel="canonical" href="{u}">'
    verify = ""
    if GOOGLE_SITE_VERIFICATION:
        verify += f'\n<meta name="google-site-verification" content="{E(GOOGLE_SITE_VERIFICATION)}">'
    if BING_SITE_VERIFICATION:
        verify += f'\n<meta name="msvalidate.01" content="{E(BING_SITE_VERIFICATION)}">'
    return f"""<!DOCTYPE html>
<html lang="en-IN" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">{robots}{canonical}{verify}
<meta name="theme-color" content="#020D34">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{u}">
<meta property="og:site_name" content="Altherix">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="{og_w}">
<meta property="og:image:height" content="{og_h}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{SITE}{og_image}">
<link rel="icon" href="/assets/icon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/icon-180.png">
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v={V}">
<script src="/assets/site.js?v={V}" defer></script>{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def nav(active=""):
    cur = ' aria-current="page"'
    links = "".join(f'<li><a href="{h}"{cur if k == active else ""}>{n}</a></li>' for n, h, k in NAV)
    mlinks = "".join(f'<a href="{h}">{n}</a>' for n, h, k in NAV)
    return f"""<header class="nav">
  <div class="ct">
    <a class="brand" href="/" aria-label="Altherix, home"><img src="/assets/mark-96.webp" width="28" height="28" alt="">ALTHERIX</a>
    <nav aria-label="Main"><ul class="nav-links">{links}</ul></nav>
    <a class="btn btn-p nav-cta" href="/#contact">Talk to an Engineer</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  <nav aria-label="Mobile">{mlinks}</nav>
  <a class="btn btn-p" href="/#contact">Talk to an Engineer</a>
  <div class="mm-meta"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a></div>
</div>
"""

def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    svc += '<li><a href="/services/enterprise-integration/#cloud">Cloud &amp; DevOps</a></li>'
    ind = "".join(f'<li><a href="/#build">{n}</a></li>' for n, *_ in BUILDS)
    return f"""<footer class="foot">
  <div class="ct">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="brand" href="/"><img src="/assets/mark-96.webp" width="28" height="28" alt="" loading="lazy">ALTHERIX</a>
        <p class="foot-tag">Modern Software.<br>Intelligent Systems.<br>Real Business Value.</p>
        <p class="foot-sub meta">Transforming Software, Amplifying Value.</p>
        <p class="foot-sub meta">Coonoor, Tamil Nadu, India. Platforms in production on Azure in the UK.</p>
      </div>
      <div><h2 class="label">Services</h2><ul>{svc}</ul></div>
      <div><h2 class="label">What we build</h2><ul>{ind}</ul></div>
      <div><h2 class="label">Company</h2><ul><li><a href="/#about">About</a></li><li><a href="/case-studies/">Case Studies</a></li><li><a href="/products/">Products</a></li><li><a href="/careers.html">Careers</a></li><li><a href="/#contact">Contact</a></li></ul></div>
      <div><h2 class="label">Contact</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li><li><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a></li></ul></div>
    </div>
    <div class="foot-bot meta">
      <span>© <span data-year>2026</span> Altherix Solutions</span>
      <span>Coonoor, Tamil Nadu, India</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

ORG = {
  "@context": "https://schema.org", "@type": ["Organization", "ProfessionalService"], "name": "Altherix Solutions",
  "alternateName": "Altherix", "url": SITE + "/", "logo": SITE + "/assets/icon-512.png",
  "slogan": "Transforming Software, Amplifying Value.",
  "email": EMAIL, "telephone": "+91-8152923515", "sameAs": [LINKEDIN], "areaServed": ["IN", "GB"],
  "address": {"@type": "PostalAddress", "streetAddress": "1247 N1, LN Gardens, Stanley Park, Ottupattarai",
              "addressLocality": "Coonoor", "addressRegion": "Tamil Nadu", "postalCode": "643105", "addressCountry": "IN"},
}

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def crumbs(items):
    parts = [f'<a href="{u}">{E(n)}</a>' for n, u in items[:-1]] + [f'<span aria-current="page">{E(items[-1][0])}</span>']
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">/</span>'.join(parts) + '</nav>'

# ── hero visual ──────────────────────────────────────────────────────────────
def hero_svg():
    W, H = 440, 470
    tiers = [("Experience", 40, [150, 240, 330, 420]),
             ("Apps", 135, [190, 300, 410]),
             ("APIs · AI", 230, [140, 210, 280, 350, 420]),
             ("Data", 325, [190, 300, 410]),
             ("Cloud", 420, [245, 355])]
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="viz-t"><title id="viz-t">System layers: experience, applications, APIs and AI, data, and cloud, connected by data flows.</title>']
    for name, y, xs in tiers:
        ti = [t[0] for t in tiers].index(name)
        out.append(f'<g class="viz-row" style="--t:{ti}"><text class="viz-label" x="0" y="{y+3.5}">{E(name)}</text>'
                   f'<line class="viz-tier" x1="118" y1="{y}" x2="{W}" y2="{y}"/></g>')
    paths = []
    for a in range(len(tiers) - 1):
        _, y1, xs1 = tiers[a]; _, y2, xs2 = tiers[a + 1]
        for i, x1 in enumerate(xs1):
            for j, x2 in enumerate(xs2):
                if abs(i / max(1, len(xs1) - 1) - j / max(1, len(xs2) - 1)) <= 0.4:
                    my = (y1 + y2) / 2
                    paths.append(f"M{x1} {y1+6} C{x1} {my} {x2} {my} {x2} {y2-6}")
    out.append('<g class="viz-links">' + "".join(f'<path class="viz-line" d="{p}"/>' for p in paths) + '</g>')
    out.append('<g class="viz-flows">' + "".join(f'<path class="viz-flow" d="{p}" style="animation-delay:-{(k*1.3)%9:.1f}s"/>' for k, p in enumerate(paths) if k % 3 == 0) + '</g>')
    for ti, (name, y, xs) in enumerate(tiers):
        for i, x in enumerate(xs):
            if ti == 2 and i == 2:
                out.append(f'<circle class="viz-core" cx="{x}" cy="{y}" r="6" style="--t:{ti}"/>')
            else:
                out.append(f'<circle class="viz-node" cx="{x}" cy="{y}" r="5" style="--t:{ti}"/>')
    out.append("</svg>")
    return "\n".join(out)

# ── components ───────────────────────────────────────────────────────────────
IMG = {  # name: (width, height) of the 1600px version
    "office": (1600, 859), "cms-overview": (1600, 909), "cms-leaders": (1600, 767),
    "missions-dashboard": (1600, 470), "codegate-test": (1600, 955), "codegate-admin": (1600, 955),
    "art-software": (1111, 941), "art-modernization": (1600, 901), "art-ai": (1600, 901), "art-integration": (1600, 901),
    "art-cloud": (972, 881), "art-codegate": (1600, 901), "art-remote": (1600, 900), "art-404": (1600, 900),
    **{f"ind-{n}": (500, 500) for n in ["manufacturing", "healthcare", "finance", "education", "logistics", "global"]},
}

def pic(name, alt, sizes="(min-width:1240px) 1160px, 100vw", lazy=True, cls=""):
    w, h = IMG[name]
    load = ' loading="lazy"' if lazy else ''
    srcset = f"/assets/img/{name}-800.webp 800w, /assets/img/{name}-1600.webp {w}w" if w > 800 else f"/assets/img/{name}-1600.webp {w}w"
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img src="/assets/img/{name}-1600.jpg" width="{w}" height="{h}" alt="{E(alt)}"{load} decoding="async"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}></picture>')

def art(name, sizes="(min-width:1000px) 560px, 100vw", lazy=False):
    """Decorative illustration beside a page heading."""
    return f'<figure class="hero-art" aria-hidden="true">{pic(name, "", sizes, lazy)}</figure>'

SERVICE_ART = {"software-engineering": "art-software", "modernization": "art-modernization", "ai-automation": "art-ai", "enterprise-integration": "art-integration"}


def shot(name, alt, caption=None, sizes="(min-width:1240px) 1160px, 100vw"):
    """A product screenshot in a quiet browser frame."""
    cap = f'<figcaption class="meta">{E(caption)}</figcaption>' if caption else ""
    return f'<figure class="shot rv"><div class="shot-frame" aria-hidden="false">{pic(name, alt, sizes)}</div>{cap}</figure>'

def cs_panel(c):
    h = c["headline"]
    subs = "".join(f"<div><b>{E(v)}</b>{E(l)}</div>" for v, l in c["metrics"][1:3] if v != "Live")
    status = '<span class="status">Live in production</span>' if c.get("featured") else "<span></span>"
    client = f'<p class="meta">{E(c["client"])}</p>' if c.get("client") else ""
    return f"""<article class="cs rv">
  <div class="cs-metric">
    <div><div class="cs-big">{E(h[0])}</div><div class="cs-big-l">{E(h[1])}</div></div>
    <div class="cs-sub">{subs}</div>
  </div>
  <div class="cs-body">
    <div><span class="label">{E(c['category'])}</span><h3 class="h3-lg" style="margin-top:.6rem">{E(c['title'])}</h3>{client}</div>
    <div class="cs-ps"><div><span class="label">Problem</span><p>{E(c['problem'])}</p></div><div><span class="label">Solution</span><p>{E(c['solution'])}</p></div></div>
    <p class="stack-line">{dot(c['tech'][:8])}</p>
    <div class="cs-foot">{status}<a class="more" href="/case-studies/{c['slug']}/">Read the case study <span class="arr" aria-hidden="true">→</span></a></div>
  </div>
</article>"""

def cs_row(c):
    return f"""<a class="row cs-row" href="/case-studies/{c['slug']}/">
  <span class="n">{E(c['headline'][0])}<small>{E(c['headline'][1])}</small></span>
  <span><span class="label">{E(c['category'])}</span><span class="h3" style="display:block">{E(c['title'])}</span></span>
  <span class="body">{E(c['oneliner'])}</span>
  <span class="arr" aria-hidden="true">→</span>
</a>"""

def contact_section(heading="Have a difficult software problem?", lede="Whether you're modernizing a legacy platform, integrating enterprise systems, or figuring out where AI actually fits, start with a conversation with our engineering team."):
    opts = "".join(f"<option>{s['name']}</option>" for s in SERVICES) + "<option>Cloud &amp; DevOps</option><option>Not sure yet</option>"
    return f"""<section class="sec contact-sec" id="contact" aria-labelledby="contact-h">
  <div class="ct two even">
    <div class="rv">
      <span class="label">Contact</span>
      <h2 class="h2" id="contact-h" style="margin-top:1.25rem">{heading}</h2>
      <p class="lede" style="margin-top:1.25rem">{lede}</p>
      <dl class="contact-dl">
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div><dt>Phone</dt><dd><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></dd></div>
        <div><dt>LinkedIn</dt><dd><a href="{LINKEDIN}" target="_blank" rel="noopener">linkedin.com/company/altherix</a></dd></div>
        <div><dt>Office</dt><dd>{'<br>'.join(ADDRESS)}</dd></div>
      </dl>
    </div>
    <form class="form rv" id="contact-form" novalidate aria-label="Contact form">
      <div class="row2">
        <div><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
        <div><label for="f-email">Work email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      </div>
      <div class="row2">
        <div><label for="f-company">Company <span class="opt">(optional)</span></label><input id="f-company" name="company" autocomplete="organization"></div>
        <div><label for="f-topic">Area <span class="opt">(optional)</span></label><select id="f-topic" name="topic"><option value="">Choose one</option>{opts}</select></div>
      </div>
      <div><label for="f-msg">What are you working on?</label><textarea id="f-msg" name="message" required aria-describedby="f-hint"></textarea><p class="meta" id="f-hint" style="margin-top:.4rem">The system, the problem, and what a good outcome looks like.</p></div>
      <button class="btn btn-p" type="submit">Talk to an Engineer</button>
      <p class="meta">This opens your email app with the message addressed to {EMAIL}. An engineer replies within one working day.</p>
      <p class="form-ok" id="form-ok" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>"""

def sec_head(label, title, lede=None, hid=None, split=True):
    idattr = f' id="{hid}"' if hid else ""
    right = f'<p class="lede">{lede}</p>' if lede else ""
    return f'<div class="sec-hd{" split" if (split and lede) else ""} rv"><div><span class="label">{label}</span><h2 class="h2"{idattr} style="margin-top:1.25rem">{title}</h2></div>{right}</div>'

# ── HOME ─────────────────────────────────────────────────────────────────────
def home():
    path = "index.html"
    outcomes = [("2", "Production platforms", "Built and run for The Church of Pentecost", "/case-studies/"),
                ("7", "Organisational levels", "One reporting system, Global Office to local assembly", "/case-studies/missions-office-enterprise-system/"),
                ("80+", "API modules", "Church Management System on .NET 9 and Azure", "/case-studies/church-management-system/")]
    out_html = "".join(f'<a class="outcome" href="{s}"><span class="n">{n}</span><span class="l">{l}</span><span class="s">{d}</span></a>' for n, l, d, s in outcomes)

    svc_rows = ""
    for s in SERVICES:
        svc_rows += f"""<div class="row svc-row rv">
  <span class="idx">{s['n']}</span>
  <a class="svc-thumb" href="/services/{s['slug']}/" tabindex="-1" aria-hidden="true">{pic(SERVICE_ART[s['slug']], "", "(min-width:960px) 220px, 100vw")}</a>
  <div><h3 class="h3-lg">{s['name']}</h3><p class="body">{E(s['short'])}</p><p class="stack-line">{dot(s['tech'][:6])}</p><a class="more" href="/services/{s['slug']}/" aria-label="{s['name']}: learn more">Learn more <span class="arr" aria-hidden="true">→</span></a></div>
  <ul>{''.join(f'<li>{E(x)}</li>' for x in s['list'])}</ul>
</div>"""
    svc_rows += """<div class="row svc-row rv">
  <span class="idx">05</span>
  <a class="svc-thumb" href="/services/enterprise-integration/#cloud" tabindex="-1" aria-hidden="true">""" + pic("art-cloud", "", "(min-width:960px) 220px, 100vw") + """</a>
  <div><h3 class="h3-lg">Cloud &amp; DevOps</h3><p class="body">Part of every engagement, and available on its own: pipelines, hardened infrastructure and monitoring that catches problems before your users do.</p><p class="stack-line">Azure · Azure DevOps · GitHub Actions · AWS S3</p><a class="more" href="/services/enterprise-integration/#cloud" aria-label="Cloud and DevOps: learn more">Learn more <span class="arr" aria-hidden="true">→</span></a></div>
  <ul><li>CI/CD pipelines</li><li>Cloud infrastructure</li><li>Monitoring &amp; alerting</li><li>Cloud migration</li></ul>
</div>"""

    panels = "\n".join(cs_panel(CASE[s]) for s in ["church-management-system", "missions-office-enterprise-system"])

    ai_areas = [("AI grading, checked by tests", "In CodeGate, hidden tests decide whether code works. AI only scores quality against a written rubric and summarises each answer for a reviewer."),
                ("Agents behind a permission gate", "Mandate, in development: an AI agent can act on ERP data only through approved actions, and risky ones wait for a person."),
                ("Automation that needs no model", "In our client platforms, recurring events and data-completeness checks run as scheduled background jobs. No AI required."),
                ("A person can always see why", "Where AI makes a judgement, the reasoning is shown and a person can override it.")]
    ai_html = "".join(f'<div><h3 class="h3">{t}</h3><p class="body">{d}</p></div>' for t, d in ai_areas)

    layers = [("Experience", "Web apps and dashboards", ["React 18", "TypeScript", "MUI", "Alpine.js", "Chart.js"]),
              ("Applications", "Domain logic and workflows", [".NET 9", "ASP.NET Core", "Laravel 12", "PHP 8.2"]),
              ("APIs, services & AI", "Contracts between systems", ["REST", "SignalR", "Hangfire", "LLM integration"]),
              ("Data", "Records, reporting and exports", ["SQL Server", "MySQL", "EF Core", "dompdf"]),
              ("Cloud & DevOps", "Run, release and observe", ["Azure (UK South)", "Azure App Service", "Azure DevOps", "Gated releases"])]
    layer_html = "".join(f'<li class="layer"><div><h3 class="h3">{n}</h3><p class="meta">{sub}</p></div><p class="stack-line">{dot(t)}</p></li>' for n, sub, t in layers)

    inds = "".join(f'<div class="ind rv"><div class="ind-art" aria-hidden="true">{pic("ind-" + art, "", "(min-width:1080px) 360px, (min-width:760px) 45vw, 100vw")}</div><h3 class="h3">{n}</h3><p class="body">{d}</p>' + (f'<a class="more" href="{href}">{lt} <span class="arr" aria-hidden="true">→</span></a>' if href else '') + '</div>' for n, art, d, href, lt in BUILDS)


    fits = [("Your records live in spreadsheets and paper.", "Members, customers, stock or bookings tracked in Excel files and registers that nobody fully trusts.", "/case-studies/church-management-system/", "How we replaced paper registers"),
            ("Your tools don't talk to each other.", "Invoices typed in twice, reports assembled by hand, the same customer in three systems.", "/services/enterprise-integration/", "How we'd connect them"),
            ("You need reporting people can trust.", "Figures from many branches or teams, each person seeing only their part, with exports that show where numbers came from.", "/case-studies/missions-office-enterprise-system/", "Seven-level reporting we built")]
    fit_html = "".join(f'<div class="fit rv"><h3 class="h3">{a}</h3><p class="body">{b}</p><a class="more" href="{s}">{n} <span class="arr" aria-hidden="true">→</span></a></div>' for a, b, s, n in fits)
    whys = [("You work with the builders.", "No account managers or hand-offs. The engineers on your first call design, build and deploy your system."),
            ("You get our full attention.", "We take on a small number of clients at a time, so your project is never one of fifty."),
            ("Our work is live.", "Two platforms we built are in production on Azure and we still run them. We'll walk you through how they're built."),
            ("Start small, decide later.", "Begin with a written assessment or a single module. If it works, we carry on. If not, you haven't committed much.")]
    why_html = "".join(f'<div class="rv"><h3 class="h3">{a}</h3><p class="body">{b}</p></div>' for a, b in whys)
    founding_mail = f"mailto:{EMAIL}?subject=" + "Founding%20client%20rates"
    eng = [("A call with an engineer", "30 minutes, free. You describe the system and what a good outcome looks like. You talk to someone who builds, not a salesperson."),
           ("A written assessment", "We look at the existing system, code and data, and send back what we found: what's there, the risks and two or three options."),
           ("A scoped proposal", "Fixed scope, milestones and price for defined work, or a monthly team for ongoing work. You choose."),
           ("Working software every two weeks", "Each increment is deployed to a staging environment you can use, and reviewed with you before the next one starts."),
           ("Go live, then stay", "Deployment, monitoring and handover documentation. We keep supporting the system after launch.")]
    eng_html = "".join(f'<li><span class="idx">0{i+1}</span><span><b>{a}</b>{b}</span></li>' for i, (a, b) in enumerate(eng))
    principles = [("We improve before we replace.", "Existing systems often contain years of business knowledge. We modernize intelligently instead of rewriting everything unnecessarily."),
                  ("Engineers stay close to the problem.", "Architecture, development and delivery remain connected. The people who scope your system build it and support it."),
                  ("Production is the finish line.", "We care about deployment, reliability, observability and real-world operation — not just prototypes."),
                  ("Technology follows the problem.", "We choose the architecture and stack for the problem in front of us, rather than forcing every project into the same solution.")]
    pr_html = "".join(f'<div class="row pr-row rv"><span class="idx">0{i+1}</span><h3 class="h3-lg">{t}</h3><p class="body">{d}</p></div>' for i, (t, d) in enumerate(principles))

    practices = [("Security", ["Role-based access across production platforms", "Hierarchy-scoped queries: users retrieve only their own data", "Secrets kept out of code"]),
                 ("Reliability", ["Logging, monitoring and alerting", "Backups kept in good order", "Scheduled work handled by background jobs"]),
                 ("Delivery", ["CI/CD on Azure DevOps", "Gated releases to production", "Code review, with tests written alongside code"]),
                 ("Governance", ["Audit trails on enterprise platforms", "Exports stamped with scope, period and origin", "Access enforced at the data layer, not only the UI"])]
    prac_html = "".join(f'<div class="rv"><h3 class="h3">{t}</h3><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>' for t, items in practices)


    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    faq_html = "".join(f'<div class="row pr-row"><span class="idx">0{i+1}</span><h3 class="h3">{E(q)}</h3><p class="body">{E(a)}</p></div>' for i, (q, a) in enumerate(FAQ))
    jsonld = [ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "Altherix", "url": SITE + "/"}, faq_ld]
    html = head(SEO["home"]["seo_title"], SEO["home"]["seo_desc"], path, jsonld) + nav() + f"""
<main id="main">

<section class="hero" aria-labelledby="hero-h">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="ct">
    <div>
      <span class="label">Software engineering company · Ooty, India</span>
      <h1 class="h1" id="hero-h"><span>We extend, connect</span> <span>and modernize</span> <span class="sig">the systems you run.</span></h1>
      <p class="kw-sub">{E(SEO["home"]["kw_sub"])}</p>
      <p class="lede">We designed, built and still run two production platforms for The Church of Pentecost on Azure in the UK. Now we're taking on a small number of new clients.</p>
      <div class="btns">
        <a class="btn btn-p" href="#contact">Talk to an Engineer</a>
        <a class="btn btn-s" href="#work">Explore Our Work</a>
      </div>
    </div>
    <div class="hero-viz">{hero_svg()}</div>
  </div>
</section>

<section class="sec" aria-labelledby="proof-h" style="padding-top:0;border-top:0">
  <div class="ct">
    <h2 class="label" id="proof-h" style="margin-bottom:1.25rem">Live in production</h2>
    <div class="outcomes rv">{out_html}</div>
    <p class="proof-note meta">From the platforms we built and still run. Select one to read the case study.</p>
  </div>
</section>

<section class="sec" id="fit" aria-labelledby="fit-h">
  <div class="ct">
    {sec_head("Who we work with", "Three situations we're built for.", "Organisations in India and the UK with software that already matters to the business.", "fit-h")}
    <div class="fit-grid">{fit_html}</div>
    <p class="meta" style="margin-top:1.5rem">Not a fit: brochure websites, games, or projects that need to ship in days.</p>
  </div>
</section>

<section class="sec" id="why" aria-labelledby="why-h">
  <div class="ct">
    {sec_head("Why Altherix", "A small team, <span class='mute'>on purpose.</span>", "We're an early-stage company. Here's what that means for you.", "why-h")}
    <div class="grid2 why-grid">{why_html}</div>
    <div class="offer-grid">
      <div class="offer rv"><span class="label">Founding clients</span><h3 class="h3-lg">Be one of our next five clients.</h3><p class="body">We're building our client list. Our next five clients get founding-client rates, in return for a case study and a reference once the work is live.</p><a class="btn btn-p" href="{founding_mail}">Ask about founding-client rates</a></div>
      <div class="offer rv"><span class="label">Referrals</span><h3 class="h3-lg">Know someone who needs software built?</h3><p class="body">When someone you refer becomes a client, you both get 5 to 10% off.</p><a class="btn btn-s" href="#contact">Refer someone</a></div>
    </div>
  </div>
</section>

<section class="sec" id="services" aria-labelledby="svc-h">
  <div class="ct">
    {sec_head("Services", "Engineering for real&#8209;world complexity.", "The engineers who scope your system are the ones who build it, deploy it and keep it running.", "svc-h")}
    <div class="rows">{svc_rows}</div>
  </div>
</section>

<section class="sec" id="work" aria-labelledby="work-h">
  <div class="ct">
    {sec_head("Our work", "What we've built, <span class='mute'>and still run.</span>", "Two production platforms for The Church of Pentecost, an international church organisation.", "work-h")}
    <div class="shots-2">
      {shot("cms-overview", "Church Management System overview screen: transfer approvals, member, group and event totals, and a membership summary by age group.", "Church Management System, overview (names blurred)", "(min-width:1000px) 570px, 100vw")}
      {shot("missions-dashboard", "Missions Office statistics dashboard: reporting period selector, drill-down by administration, CSV and PDF export, and tabs for membership, evangelism, attendance, ministry, estates, Vision 2028 and data completeness.", "Missions Office Enterprise System, statistics dashboard", "(min-width:1000px) 570px, 100vw")}
    </div>
    <div class="cs-list">{panels}</div>
    <div class="after"><a class="btn btn-s" href="/products/">See our own products</a></div>
  </div>
</section>

<section class="sec" id="solutions" aria-labelledby="ai-h">
  <div class="ct two">
    <div class="rv">
      <span class="label">AI &amp; Automation</span>
      <h2 class="h2" id="ai-h" style="margin-top:1.25rem">AI that works in production.</h2>
      <p class="statement">AI doesn't replace good engineering. It depends on it.</p>
      <dl class="defs">
        <div><dt>Use AI</dt><dd>when the input is unstructured, the judgement is fuzzy, and a person can review what matters.</dd></div>
        <div><dt>Use software</dt><dd>when the rules are known. Invoicing, reconciliation and reminders need solid automation, not a model.</dd></div>
        <div><dt>Either way</dt><dd>it runs with access control, logging and an owner.</dd></div>
      </dl>
      <p style="margin-top:2rem"><a class="more" href="/services/ai-automation/">How we approach AI <span class="arr" aria-hidden="true">→</span></a></p>
    </div>
    <div style="align-self:start"><figure class="hero-art rv" aria-hidden="true" style="margin-bottom:clamp(28px,3vw,40px)">{pic("art-ai", "", "(min-width:1000px) 560px, 100vw")}</figure><div class="grid2 rv">{ai_html}</div></div>
  </div>
</section>

<section class="sec" id="architecture" aria-labelledby="arch-h">
  <div class="ct two">
    <div class="rv">
      <span class="label">Architecture</span>
      <h2 class="h2" id="arch-h" style="margin-top:1.25rem">Built for production.</h2>
      <p class="lede" style="margin-top:1.25rem">Every system is designed as a whole, from the screen a user touches to the pipeline that releases it. These are the layers, and what we build them with.</p>
    </div>
    <ol class="layers rv" aria-label="Architecture layers">{layer_html}</ol>
  </div>
</section>

<section class="sec" id="build" aria-labelledby="ind-h">
  <div class="ct">
    {sec_head("What we can build", "Systems for the work <span class='mute'>your business actually does.</span>", "The first we've built and run in production. The others use the same building blocks: records, workflows, integrations and reporting.", "ind-h")}
    <div class="ind-grid">{inds}</div>
  </div>
</section>

<section class="sec" id="why" aria-labelledby="why-h">
  <div class="ct">
    {sec_head("Why Altherix", "Why teams work with Altherix.", None, "why-h")}
    <div class="rows">{pr_html}</div>
  </div>
</section>

<section class="sec" id="practices" aria-labelledby="prac-h">
  <div class="ct">
    {sec_head("Engineering practices", "The unglamorous parts, <span class='mute'>done properly.</span>", "What goes into the production systems we run, as standard.", "prac-h")}
    <div class="cols4">{prac_html}</div>
  </div>
</section>

<section class="sec" id="about" aria-labelledby="about-h">
  <div class="ct two even">
    <div class="prose rv">
      <span class="label">About</span>
      <h2 class="h2" id="about-h" style="margin-top:1.25rem">Global engineering. <span class="mute">Rooted in the Nilgiris.</span></h2>
      <p>Altherix was founded in Ooty, high in the Nilgiris, and works from Coonoor in Tamil Nadu, India. It's an unusual place for an engineering company, and a deliberate one: a small team with room to do careful work, away from the churn of a large delivery centre.</p>
      <p>The work reaches well beyond the hills. The two platforms we've built so far run in production on Azure in the UK for The Church of Pentecost, an international church organisation. We're now taking on our next clients, in India, the UK and elsewhere.</p>
      <p>One conviction hasn't changed: your existing software is the backbone of your business, and it usually deserves improving before it deserves replacing.</p>
    </div>
    <div style="align-self:end">
    <figure class="photo rv">{pic("office", "The Altherix office building with the Altherix sign at the entrance, set against green hillside.", "(min-width:1000px) 570px, 100vw")}</figure>
    <dl class="facts-dl rv">
      <div><dt>Founded</dt><dd>Ooty, the Nilgiris</dd></div>
      <div><dt>Office</dt><dd>Coonoor, Tamil Nadu</dd></div>
      <div><dt>In production</dt><dd>Azure UK South</dd></div>
      <div><dt>Products</dt><dd>CodeGate · Mandate (in development)</dd></div>
      <div><dt>Company</dt><dd>Altherix Solutions</dd></div>
    </dl>
    </div>
  </div>
</section>

<section class="sec" id="process" aria-labelledby="proc-h">
  <div class="ct two">
    <div class="rv">
      <span class="label">How it works</span>
      <h2 class="h2" id="proc-h" style="margin-top:1.25rem">From first call <span class="mute">to production.</span></h2>
      <p class="lede" style="margin-top:1.25rem">What happens after you get in touch, and what you get at each step.</p>
      <div class="btns" style="margin-top:2rem"><a class="btn btn-p" href="#contact">Book the first call</a></div>
    </div>
    <ol class="steps rv">{eng_html}</ol>
  </div>
</section>

<section class="sec" id="faq" aria-labelledby="faq-h">
  <div class="ct">
    {sec_head("FAQ", "Common questions.", None, "faq-h")}
    <div class="rows">{faq_html}</div>
  </div>
</section>

{contact_section()}

</main>
""" + footer()
    write(path, html); PAGES.append((path, "1.0"))

# ── CASE STUDIES INDEX ───────────────────────────────────────────────────────
def cases_index():
    path = "case-studies/index.html"
    feat = CASES
    html = head(SEO["case-studies"]["seo_title"], SEO["case-studies"]["seo_desc"], path,
                [ORG, crumbs_ld([("Home", "/"), ("Case Studies", "/case-studies/")])]) + nav("case-studies") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  {crumbs([("Home", "/"), ("Case Studies", "/case-studies/")])}
  <span class="label">Case studies</span>
  <h1 class="h1">Our work so far.</h1>
  <p class="lede">Two production platforms for The Church of Pentecost. We designed, built and deployed both, and we still support them.</p>
</div></header>
<section class="sec"><div class="ct">
  <h2 class="label" style="margin-bottom:1.25rem">Client work</h2>
  <div class="cs-list">{''.join(cs_panel(c) for c in feat)}</div>
</div></section>
<section class="sec"><div class="ct">
  {sec_head("Our own products", "Built for problems <span class='mute'>we had ourselves.</span>", None, "more-h")}
  <div class="rows"><a class="row cs-row" href="/products/#codegate"><span class="n">In use<small>Early access</small></span><span><span class="label">Hiring</span><span class="h3" style="display:block">CodeGate</span></span><span class="body">Online coding assessment: hidden tests decide correctness and AI grades quality.</span><span class="arr" aria-hidden="true">→</span></a><a class="row cs-row" href="/products/#mandate"><span class="n">Building<small>Early access soon</small></span><span><span class="label">AI governance</span><span class="h3" style="display:block">Mandate</span></span><span class="body">A safe gateway between AI agents and your ERP, databases and in-house systems.</span><span class="arr" aria-hidden="true">→</span></a></div>
</div></section>
{contact_section("Discuss a similar problem.", "Tell us about the system you're working with and what a good outcome looks like. An engineer will reply.")}
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.9"))

# ── CASE STUDY PAGE ──────────────────────────────────────────────────────────
def case_page(c):
    path = f"case-studies/{c['slug']}/index.html"
    svc = SERVICE[c["related_service"]]
    toc = [("summary", "Summary"), ("results", "Results")] + ([("screens", "Screens")] if c.get("shots") else []) + [("challenge", "The challenge"), ("approach", "The approach"), ("architecture", "Architecture"),
           ("engineering", "Engineering"), ("technology", "Technology"), ("impact", "Impact")]
    others = [x for x in CASES if x["slug"] != c["slug"]]
    close = [x for x in others if x["industry"] == c["industry"] or x["related_service"] == c["related_service"]]
    related = (close + [x for x in others if x not in close])[:2]
    published, modified = git_dates(path)
    published = published or TODAY
    facts = [("Category", c["category"]), ("Industry", c["industry"])]
    if c.get("client"): facts.insert(0, ("Client", c["client"]))
    if c.get("featured"): facts.append(("Status", "Live in production"))
    jsonld = [ORG, crumbs_ld([("Home", "/"), ("Case Studies", "/case-studies/"), (c["title"], f"/case-studies/{c['slug']}/")]),
              {"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "description": c["oneliner"],
               "author": {"@type": "Organization", "name": "Altherix Solutions"},
               "publisher": {"@type": "Organization", "name": "Altherix Solutions", "logo": {"@type": "ImageObject", "url": SITE + "/assets/icon-512.png"}},
               "image": SITE + f"/assets/og/{c['slug']}.jpg", "mainEntityOfPage": url_for(path),
               "datePublished": published, "dateModified": "__MODIFIED__"}]
    rel = f'<section class="sec"><div class="ct">{sec_head("More work", "Related case studies", None, "rel-h")}<div class="rows">{"".join(cs_row(r) for r in related)}</div></div></section>' if related else ""
    html = head(f"{c['title']}: Case Study | Altherix", c["seo_desc"], path, jsonld, "article", og_image=f"/assets/og/{c['slug']}.jpg") + nav("case-studies") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  {crumbs([("Home", "/"), ("Case Studies", "/case-studies/"), (c['title'], "")])}
  <span class="label">{E(c['category'])}</span>
  <h1 class="h1">{E(c['title'])}</h1>
  <p class="lede">{E(c['oneliner'])}</p>
  <dl class="facts">{''.join(f'<div><dt>{k}</dt><dd>{E(v)}</dd></div>' for k, v in facts)}</dl>
</div></header>
<section class="sec"><div class="ct article">
  <div class="read-progress" aria-hidden="true"></div>
  <nav class="toc" aria-label="On this page">{''.join(f'<a href="#{i}">{t}</a>' for i, t in toc)}</nav>
  <div>
    <div class="block" id="summary"><h2 class="h3-lg">Summary</h2><p>{E(c['summary'])}</p></div>
    <div class="block" id="results"><h2 class="h3-lg">Results</h2><div class="results-band metrics rv">{''.join(f'<div><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in c['metrics'])}</div></div>
    {('<div class="block" id="screens"><h2 class="h3-lg">Screens</h2><div class="shots-stack">' + "".join(shot(n, a, cap, "(min-width:1000px) 760px, 100vw") for n, a, cap in c["shots"]) + '</div></div>') if c.get("shots") else ""}
    <div class="block" id="challenge"><h2 class="h3-lg">The challenge</h2>{''.join(f'<p>{E(p)}</p>' for p in c['challenge'])}</div>
    <div class="block" id="approach"><h2 class="h3-lg">The approach</h2><ul class="plist">{''.join(f'<li><b>{E(a)}.</b> {E(b)}</li>' for a, b in c['approach'])}</ul></div>
    <div class="block" id="architecture"><h2 class="h3-lg">Architecture</h2><ol class="arch-flow rv" aria-label="Architecture, in order of data flow">{''.join(f'<li><span class="arch-n">{E(a)}</span><span class="arch-d">{E(b)}</span></li>' for a, b in c['architecture'])}</ol></div>
    <div class="block" id="engineering"><h2 class="h3-lg">Engineering</h2><dl class="kv">{''.join(f'<div><dt>{E(a)}</dt><dd>{E(b[0].upper() + b[1:])}.</dd></div>' for a, b in c['engineering'])}</dl></div>
    <div class="block" id="technology"><h2 class="h3-lg">Technology</h2><p class="stack-line" style="font-size:.875rem">{dot(c['tech'])}</p></div>
    <div class="block" id="impact"><h2 class="h3-lg">Impact</h2><p>{E(c['impact'])}</p><p style="margin-top:1.5rem"><a class="more" href="/services/{svc['slug']}/">Related service: {svc['name']} <span class="arr" aria-hidden="true">→</span></a></p></div>
  </div>
</div></section>
{rel}
{contact_section("Discuss a similar problem.", "If this looks like something you're dealing with, tell us about your system. An engineer will reply.")}
</main>
""" + footer()
    # dateModified: last commit date, or today if this build changes the page.
    old = committed_text(path)
    norm = lambda t: re.sub(r'"date(Published|Modified)": "[^"]*"', '', t or "")
    unchanged = old is not None and norm(old) == norm(html.replace('"__MODIFIED__"', '"x"'))
    html = html.replace("__MODIFIED__", (modified or TODAY) if unchanged else TODAY)
    write(path, html); PAGES.append((path, "0.8"))

# ── SERVICE PAGE ─────────────────────────────────────────────────────────────
def service_page(s):
    path = f"services/{s['slug']}/index.html"
    others = "".join(f'<a class="row cs-row" href="/services/{o["slug"]}/"><span class="idx">{o["n"]}</span><span class="h3" style="display:block">{o["name"]}</span><span class="body">{E(o["short"])}</span><span class="arr" aria-hidden="true">→</span></a>' for o in SERVICES if o["slug"] != s["slug"])
    cloud = ""
    if s.get("cloud"):
        cl = s["cloud"]
        cloud = f'<section class="sec" id="cloud"><div class="ct two"><div class="rv"><span class="label">Also</span><h2 class="h2" style="margin-top:1.25rem">{cl["title"]}</h2><p class="lede" style="margin-top:1.25rem">{E(cl["text"])}</p></div><ul class="plist rv" style="align-self:start">{"".join(f"<li>{E(x)}</li>" for x in cl["list"])}</ul></div></section>'
    jsonld = [ORG, crumbs_ld([("Home", "/"), ("Services", "/#services"), (s["name"], f"/services/{s['slug']}/")]),
              {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": s["short"], "provider": {"@type": "Organization", "name": "Altherix Solutions", "url": SITE + "/"}, "areaServed": ["IN", "GB"]}]
    h1 = s["h1"].replace("<em>", '<span class="mute">').replace("</em>", "</span>")
    html = head(s["seo_title"], s["seo_desc"], path, jsonld, og_image=f"/assets/og/{s['slug']}.jpg") + nav("services") + f"""
<main id="main">
<header class="page-hero"><div class="ct hero-split"><div>
  {crumbs([("Home", "/"), ("Services", "/#services"), (s['name'], "")])}
  <span class="label">{s['name']}</span>
  <h1 class="h1">{h1}</h1>
  <p class="kw-sub">{E(s['kw_sub'])}</p>
  <p class="lede">{E(s['lede'])}</p>
  <div class="btns"><a class="btn btn-p" href="#contact">Talk to an Engineer</a><a class="btn btn-s" href="#work">Relevant work</a></div>
</div>{art(SERVICE_ART[s['slug']])}</div></header>
<section class="sec"><div class="ct two">
  <div class="rv"><span class="label">The problem</span><h2 class="h2" style="margin-top:1.25rem">Why this is harder than it looks.</h2></div>
  <div class="prose rv">{''.join(f'<p>{E(p)}</p>' for p in s['problem'])}</div>
</div></section>
<section class="sec"><div class="ct two">
  <div class="rv"><span class="label">Approach</span><h2 class="h2" style="margin-top:1.25rem">How we work.</h2></div>
  <ol class="steps rv">{''.join(f'<li><span class="idx">0{i+1}</span><span><b>{E(a)}</b>{E(b)}</span></li>' for i, (a, b) in enumerate(s['approach']))}</ol>
</div></section>
<section class="sec"><div class="ct two">
  <div class="rv"><span class="label">Capabilities</span><h2 class="h2" style="margin-top:1.25rem">What we do.</h2><p class="stack-line" style="margin-top:1.5rem">{dot(s['tech'])}</p></div>
  <dl class="kv rv">{''.join(f'<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in s['caps'])}</dl>
</div></section>
{cloud}
<section class="sec" id="work"><div class="ct">
  {sec_head("Relevant case studies", s.get('cases_title', 'Where we have done this.'), E(s['cases_note']) if s.get('cases_note') else None, "work-h")}
  <div class="rows">{''.join(cs_row(CASE[x]) for x in s['cases'])}</div>
</div></section>
<section class="sec"><div class="ct">
  {sec_head("Other services", "Related capabilities", None, "oth-h")}
  <div class="rows">{others}</div>
</div></section>
{contact_section()}
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.8"))

# ── CAREERS ──────────────────────────────────────────────────────────────────
def careers():
    path = "careers.html"
    def apply(subject, body):
        return f'mailto:{EMAIL}?subject={quote(subject)}&amp;body={quote(body)}'
    std_body = "Hello Altherix team,\n\nI'd like to apply for the {r} role.\n\nA little about me:\n\n\nLinks (GitHub / portfolio / LinkedIn):\n\n\nMy CV is attached.\n\nThank you,"
    roles = [
      dict(t="Full Stack Development Intern", tag="New", facts="Fully remote · 2 or 3 months · Stipend · Paid 3-day onsite in Ooty",
           about="A fully remote internship of two or three months, with a stipend. You'll work on real client projects from week one, with a senior engineer as your mentor. Our team is based in Coonoor, near Ooty, and interns join us for a paid three-day onsite in Ooty.",
           do=["Ship features into a live codebase under close review", "Write tests and documentation alongside your code", "Learn how professional delivery runs, from estimate to release"],
           want=["Fluency in at least one language: C#, Java, PHP, Python or JavaScript", "Something you've built that you can walk us through, however small", "Preferred: BSc or BCA with a Computer Science major"],
           nice=None, how=f"Send your CV and a link to your work to {EMAIL} with the subject “Full Stack Internship”.",
           href=apply("Full Stack Internship", "Hello Altherix team,\n\nI'd like to apply for the Full Stack Development Internship.\n\nA little about me:\n\n\nLink to my work:\n\n\nMy CV is attached.\n\nThank you,"), open=True),
      dict(t="Senior Full-Stack Engineer, .NET & React", facts="Ooty · Hybrid · Full time · 5+ years",
           about="You'll lead delivery on enterprise platforms built with ASP.NET Core and React: designing the data model, building the API, shaping the front end, and taking it through to an Azure deployment. This is our most senior individual-contributor track.",
           do=["Design and build REST APIs with ASP.NET Core and Entity Framework Core", "Build front ends in React and TypeScript with a considered component architecture", "Model relational schemas and write queries that stay fast as data grows", "Work directly with clients to turn ambiguous requirements into a shippable scope", "Review other engineers' work and raise the standard of the codebase"],
           want=["Five or more years building and shipping production web applications", "Strong C# and .NET, with real Entity Framework and SQL Server experience", "Confident in React, TypeScript and modern front-end tooling", "Comfortable owning a deployment: CI/CD pipelines, cloud hosting, diagnosing production issues", "Clear written and spoken communication; you'll be in front of clients"],
           nice=["Azure services: App Service, SQL, Blob Storage, DevOps pipelines", "Background jobs and real-time messaging (Hangfire, SignalR or equivalents)", "Experience modernising a legacy codebase without a rewrite"],
           href=apply("Application: Senior Full-Stack Engineer (.NET & React)", std_body.format(r="Senior Full-Stack Engineer"))),
      dict(t="Full-Stack Engineer, PHP & Laravel", facts="Ooty · Hybrid · Full time · 2–5 years",
           about="We build reporting and operational platforms on Laravel for clients who need a lot of domain logic handled correctly. You'll work across the stack: schema, application logic, and the dashboards people look at every day.",
           do=["Build features across Laravel applications: migrations, models, services, controllers and Blade views", "Write aggregation and reporting logic where correctness genuinely matters", "Build interactive dashboards and data visualisations for non-technical users", "Implement role-based access control and audit trails", "Write tests that give us confidence to deploy on a Friday"],
           want=["Two or more years with PHP and a modern framework, ideally Laravel", "Solid relational database skills: you can read a slow query and fix it", "Working knowledge of JavaScript and at least one front-end approach", "Care about data accuracy and edge cases, not just the happy path"],
           nice=["Charting libraries, PDF and spreadsheet generation", "Experience with multi-tenant or hierarchical permission models"],
           href=apply("Application: Full-Stack Engineer (PHP & Laravel)", std_body.format(r="Full-Stack Engineer (Laravel)"))),
      dict(t="Cloud & DevOps Engineer", facts="Ooty · Hybrid · Full time · 3+ years",
           about="You'll own how our clients' systems get built, released and observed: pipelines, environments, cost, and the alerting that tells us something is wrong before the client does.",
           do=["Build and maintain CI/CD pipelines across Azure DevOps and GitHub Actions", "Provision and harden cloud infrastructure, primarily on Azure", "Set up monitoring, logging and alerting for production workloads", "Lead migrations from on-premise or shared hosting into the cloud", "Keep secrets, backups and access controls in good order"],
           want=["Three or more years in a DevOps, platform or SRE role", "Hands-on Azure experience; AWS or GCP also considered", "Comfortable scripting in Bash, PowerShell or Python", "Containers and infrastructure-as-code in day-to-day use"],
           nice=None, href=apply("Application: Cloud & DevOps Engineer", std_body.format(r="Cloud & DevOps Engineer"))),
    ]
    def ul(x): return "<ul>" + "".join(f"<li>{E(i)}</li>" for i in x) + "</ul>"
    rhtml = ""
    for r in roles:
        tag = f'<span class="role-tag">{r["tag"]}</span>' if r.get("tag") else ""
        rhtml += f"""<details class="role"{' open' if r.get('open') else ''}>
  <summary><div><h3 class="h3">{E(r['t'])}{tag}</h3><p class="role-facts">{E(r['facts'])}</p></div><span class="role-chev" aria-hidden="true">+</span></summary>
  <div class="role-body">
    <span class="label">About the role</span><p>{E(r['about'])}</p>
    <span class="label">What you'll do</span>{ul(r['do'])}
    <span class="label">What we're looking for</span>{ul(r['want'])}
    {'<span class="label">Nice to have</span>' + ul(r['nice']) if r.get('nice') else ''}
    {'<span class="label">How to apply</span><p>' + E(r['how']) + '</p>' if r.get('how') else ''}
    <a class="btn btn-p" href="{r['href']}">Apply for this role</a>
  </div>
</details>"""
    why = [("You own the whole problem", "Engineers here talk to clients, shape the solution, build it and see it through to deployment."),
           ("Real systems, real users", "The platforms we build run production workloads for organisations that depend on them."),
           ("Breadth by design", "Consulting means variety: .NET one quarter, Laravel the next, an Azure migration after that."),
           ("Senior people to learn from", "A deliberately small team with deep enterprise and architecture experience. Reviews are thorough; mentoring is direct.")]
    steps = [("Application", "Send your CV and a few lines about what you've built. We read every one and reply within a week."),
             ("Intro call", "Thirty minutes with an engineer: your background, our work, and whether the fit makes sense both ways."),
             ("Technical conversation", "We work through a realistic problem together and discuss code you've written. No whiteboard puzzles, no unpaid take-home projects."),
             ("Offer", "A final conversation on scope, expectations and compensation, then a written offer.")]
    bene = [("Paid intern onsite", "Interns spend three paid days with the team in Ooty."),
            ("Hybrid working", "Full-time roles split between our Nilgiris office and home, arranged around delivery."),
            ("Learning budget", "An annual allowance for certifications, courses and conferences, and time to use it."),
            ("Health cover", "Medical insurance for you and your immediate family."),
            ("Client-facing work", "You're in the room where decisions are made."),
            ("Honest estimates", "We push back on unrealistic dates. Crunch is a planning failure, not a culture.")]
    jobs = [{"@context": "https://schema.org", "@type": "JobPosting", "title": "Full Stack Development Intern",
             "description": roles[0]["about"], "employmentType": "INTERN", "datePosted": "2026-09-30",
             "hiringOrganization": {"@type": "Organization", "name": "Altherix Solutions", "sameAs": LINKEDIN, "logo": SITE + "/assets/icon-512.png"},
             "jobLocationType": "TELECOMMUTE", "applicantLocationRequirements": {"@type": "Country", "name": "India"},
             "educationRequirements": "BSc / BCA with a Computer Science major preferred"}]
    html = head(SEO["careers"]["seo_title"], SEO["careers"]["seo_desc"], path,
                [ORG, crumbs_ld([("Home", "/"), ("Careers", "/careers.html")])] + jobs) + nav("careers") + f"""
<main id="main">
<header class="page-hero"><div class="ct hero-split"><div>
  {crumbs([("Home", "/"), ("Careers", "")])}
  <span class="label">Careers</span>
  <h1 class="h1">Small team. <span class="mute">Serious systems.</span></h1>
  <p class="lede">Our work goes into production and stays there: enterprise platforms, reporting systems and integrations that organisations depend on every day. If you want ownership rather than a ticket queue, we should talk.</p>
  <div class="btns"><a class="btn btn-p" href="#roles">See open roles</a><a class="more" href="{LINKEDIN}" target="_blank" rel="noopener">Follow Altherix on LinkedIn <span class="arr" aria-hidden="true">→</span></a></div>
</div>{art("art-remote")}</div></header>

<section class="sec" id="roles" aria-labelledby="roles-h"><div class="ct">
  {sec_head("Open roles", "Where we're hiring.", "Our team is based in Coonoor, near Ooty. Full-time roles are hybrid; internships are fully remote.", "roles-h")}
  <div class="roles">{rhtml}</div>
  <p class="body" style="margin-top:2rem">Nothing quite fits? Write to <a href="mailto:{EMAIL}">{EMAIL}</a> and tell us what you'd want to work on.</p>
</div></section>

<section class="sec"><div class="ct">
  {sec_head("Working here", "What the work is actually like.", None, "why-h")}
  <figure class="photo rv" style="margin-bottom:clamp(40px,5vw,64px)">{pic("office", "The Altherix office in the Nilgiris, with the Altherix sign at the entrance.")}</figure>
  <div class="grid2">{''.join(f'<div class="rv"><h3 class="h3">{t}</h3><p class="body">{d}</p></div>' for t, d in why)}</div>
</div></section>

<section class="sec"><div class="ct two">
  <div class="rv"><span class="label">How we hire</span><h2 class="h2" style="margin-top:1.25rem">Four steps. <span class="mute">No trick questions.</span></h2><p class="lede" style="margin-top:1.25rem">Usually two to three weeks, and you'll hear from us at every stage.</p></div>
  <ol class="steps rv">{''.join(f'<li><span class="idx">0{i+1}</span><span><b>{t}</b>{d}</span></li>' for i, (t, d) in enumerate(steps))}</ol>
</div></section>

<section class="sec"><div class="ct two">
  <div class="rv"><span class="label">The package</span><h2 class="h2" style="margin-top:1.25rem">What we offer.</h2></div>
  <dl class="kv rv">{''.join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in bene)}</dl>
</div></section>

<section class="sec"><div class="ct cta-end rv">
  <div><h2 class="h2">Think you'd fit in here?</h2><p class="lede">Send your CV and a short note about the work you want to do. Three honest paragraphs beat a keyword-stuffed profile.</p></div>
  <div class="btns"><a class="btn btn-p" href="{apply('General application', std_body.format(r='a suitable'))}">Email {EMAIL}</a></div>
</div></section>
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.7"))

# ── PRODUCTS ─────────────────────────────────────────────────────────────────
def products():
    path = "products/index.html"
    def mail(subject, body):
        return f"mailto:{EMAIL}?subject={quote(subject)}&amp;body=" + quote(body)
    mailto = mail("Mandate", "Hello Altherix team,\n\nI'd like early access to Mandate.\n\nCompany:\nSystems we'd like AI agents to work with:\n\nThank you,")
    cg_mail = mail("CodeGate", "Hello Altherix team,\n\nI'd like to try CodeGate for our hiring.\n\nCompany:\nRoles we're hiring for:\nCandidates per round (approx.):\n\nThank you,")
    cg_feats = [("Private, timed tests", "Each candidate gets a single-use link by email. The timer runs on the server, work autosaves, and answers submit at time-up."),
                ("Tests decide correctness", "Hidden test cases score whether the code works. The AI can't change that part of the score."),
                ("AI grades the rest", "Edge cases, code quality and efficiency are scored against a written rubric, with a short summary of each answer."),
                ("Signals, not guesswork", "Tab switches, pastes and copies are logged, and follow-up questions are generated about each candidate's own code.")]
    cg_score = [("4", "Correctness, from hidden tests"), ("2", "Edge cases"), ("2", "Code quality"), ("2", "Efficiency")]
    cg_flow = [("Invite", "Add candidates. Each one gets a private test link by email."),
               ("Test", "Candidates solve real-world problems in a browser code editor, with sample tests they can run."),
               ("Grade", "One click runs the hidden tests and AI-grades every answer."),
               ("Shortlist", "Rank candidates by score, review the flags, and use the generated questions on a short follow-up call.")]
    feats = [("Works with what you run", "ERP, SQL databases and in-house applications, made usable by AI agents."),
             ("Your permissions, not new ones", "Agents see only what their user is allowed to see."),
             ("A person approves risky actions", "Writing data, sending documents or moving money waits for approval."),
             ("Every action on record", "Each request and change is logged and can be replayed.")]
    flow = [("An AI agent asks", "An assistant wants to read a record or take an action in one of your systems."),
            ("Mandate checks", "Is this user allowed? Does this action need approval? The request is logged either way."),
            ("Your system responds", "Only permitted, approved actions reach the system. Everything else stops at Mandate.")]
    pub = {"@type": "Organization", "name": "Altherix Solutions", "url": SITE + "/"}
    jsonld = [ORG, crumbs_ld([("Home", "/"), ("Products", "/products/")]),
              {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "CodeGate by Altherix", "url": SITE + "/products/#codegate",
               "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
               "description": "An online coding assessment that ranks candidates on the code they write, using hidden tests and AI grading.", "publisher": pub},
              {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Mandate by Altherix", "url": SITE + "/products/#mandate",
               "applicationCategory": "BusinessApplication", "description": "A safe way to connect AI agents to the systems your business already runs on.", "publisher": pub}]
    index = [("codegate", "CodeGate", "In use · Early access", "Rank candidates on the code they write, using hidden tests and AI grading."),
             ("mandate", "Mandate", "In development", "A safe way to connect AI agents to the systems your business already runs on.")]
    index_html = "".join(f'<a class="row cs-row" href="#{a}"><span class="label">{st}</span><span class="h3" style="display:block">{n} <span class="mute">by Altherix</span></span><span class="body">{d}</span><span class="arr" aria-hidden="true">↓</span></a>' for a, n, st, d in index)
    html = head(SEO["products"]["seo_title"], SEO["products"]["seo_desc"], path, jsonld) + nav("products") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  {crumbs([("Home", "/"), ("Products", "")])}
  <span class="label">Products</span>
  <h1 class="h1">What we're building.</h1>
  <p class="lede">Products that come out of the problems we solve, for clients and for ourselves, built with the same engineering discipline.</p>
  <div class="rows" style="margin-top:2.5rem">{index_html}</div>
</div></header>

<section class="sec" id="codegate" aria-labelledby="codegate-h"><div class="ct">
  <figure class="product-fig rv" aria-hidden="true">{pic("art-codegate", "")}</figure>
  <div class="two">
    <div class="rv">
      <span class="label">In use · Early access</span>
      <h2 class="h2" id="codegate-h" style="margin-top:1.25rem">CodeGate <span class="mute">by Altherix</span></h2>
      <p class="statement">Rank candidates on the code they write, not the CV they send.</p>
      <p class="lede" style="margin-top:1.25rem">CodeGate is an online coding assessment. Candidates solve real-world problems in a timed browser editor, and hidden tests plus AI grading turn every answer into a score you can rank.</p>
      <div class="btns" style="margin-top:2rem"><a class="btn btn-p" href="{cg_mail}">Try CodeGate</a></div>
      <p class="meta" style="margin-top:.9rem">Built for our own hiring rounds. JavaScript today, more languages planned.</p>
    </div>
    <div class="grid2 rv" style="align-self:start">{''.join(f'<div><h3 class="h3">{t}</h3><p class="body">{d}</p></div>' for t, d in cg_feats)}</div>
  </div>
  <div class="shots-2" style="margin:clamp(48px,6vw,80px) 0 0">
    {shot("codegate-test", "CodeGate candidate screen: the question and rules on the left, a code editor with the candidate's solution on the right, a countdown timer and a Submit button.", "Candidate view: timed editor with sample tests (demo data)", "(min-width:1000px) 570px, 100vw")}
    {shot("codegate-admin", "CodeGate admin screen: test status, candidate counts, average score out of 20, an invite form and a ranked candidate list with scores, flags and decisions.", "Admin view: invite, track and rank candidates (demo data)", "(min-width:1000px) 570px, 100vw")}
  </div>
</div></section>

<section class="sec" aria-labelledby="cg-how-h"><div class="ct two">
  <div class="rv">
    <span class="label">How CodeGate scores</span>
    <h2 class="h2" id="cg-how-h" style="margin-top:1.25rem">Ten points per question. <span class="mute">The tests decide what works.</span></h2>
    <div class="metrics" style="margin-top:2rem">{''.join(f'<div><b>{v}</b><span>{l}</span></div>' for v, l in cg_score)}</div>
    <p class="meta" style="margin-top:1rem">Correctness comes only from hidden tests. AI scores the other six points against a written rubric.</p>
  </div>
  <ol class="steps rv">{''.join(f'<li><span class="idx">0{i+1}</span><span><b>{t}</b>{d}</span></li>' for i, (t, d) in enumerate(cg_flow))}</ol>
</div></section>

<section class="sec" id="mandate" aria-labelledby="mandate-h"><div class="ct">
  <figure class="product-fig rv">
    <picture>
      <source type="image/webp" srcset="/assets/mandate-hero-720.webp 720w, /assets/mandate-hero.webp 1200w" sizes="(min-width:1240px) 1160px, 100vw">
      <img src="/assets/mandate-hero.jpg" width="1200" height="674" alt="Illustration: business systems on one side and an AI agent on the other, connected through a gate where some requests pass and one is held for approval." loading="lazy" decoding="async">
    </picture>
  </figure>
  <div class="two">
    <div class="rv">
      <span class="label">In development · Early access soon</span>
      <h2 class="h2" id="mandate-h" style="margin-top:1.25rem">Mandate <span class="mute">by Altherix</span></h2>
      <p class="statement">Your ERP is about to get an AI colleague. Who decides what it can do?</p>
      <p class="lede" style="margin-top:1.25rem">Mandate is a safe way to connect AI agents to the systems your business already runs on.</p>
      <div class="btns" style="margin-top:2rem"><a class="btn btn-p" href="{mailto}">Request early access</a></div>
      <p class="meta" style="margin-top:.9rem">Or email {EMAIL} with the subject &ldquo;Mandate&rdquo;.</p>
    </div>
    <div class="grid2 rv" style="align-self:start">{''.join(f'<div><h3 class="h3">{t}</h3><p class="body">{d}</p></div>' for t, d in feats)}</div>
  </div>
</div></section>

<section class="sec" aria-labelledby="how-h"><div class="ct two">
  <div class="rv"><span class="label">How Mandate works</span><h2 class="h2" id="how-h" style="margin-top:1.25rem">AI that works inside your systems, <span class="mute">only within its mandate.</span></h2></div>
  <ol class="steps rv">{''.join(f'<li><span class="idx">0{i+1}</span><span><b>{t}</b>{d}</span></li>' for i, (t, d) in enumerate(flow))}</ol>
</div></section>

<section class="sec"><div class="ct cta-end rv">
  <div><h2 class="h2">Want to use one of these early?</h2><p class="lede">Tell us which product you're interested in and what you'd use it for. An engineer will reply.</p></div>
  <div class="btns"><a class="btn btn-p" href="{cg_mail}">Try CodeGate</a><a class="btn btn-s" href="{mailto}">Mandate early access</a></div>
</div></section>
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.8"))

def notfound():
    html = head("Page not found | Altherix", "This page doesn't exist.", "404.html", noindex=True) + nav() + """
<main id="main"><section class="nf page-hero"><div class="ct hero-split"><div>
  <span class="label">404</span><h1 class="h1">This page isn't in production.</h1>
  <p class="lede">The link may be old or mistyped.</p>
  <div class="btns"><a class="btn btn-p" href="/">Go to the homepage</a><a class="btn btn-s" href="/case-studies/">View case studies</a></div>
</div>""" + art("art-404") + """</div></section></main>
""" + footer()
    write("404.html", html)

def seo_files():
    # lastmod = date of the last commit that changed the page, or today if this build changed it.
    urls = "".join(f"<url><loc>{url_for(p)}</loc><lastmod>{last_modified(p)}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    llms = [f"# Altherix", "",
            "> Altherix Solutions is a software engineering company in Coonoor, Tamil Nadu, India (founded in Ooty, the Nilgiris). "
            "It builds custom software, modernizes existing applications, adds automation and AI, and integrates business systems. "
            "Its production work so far is two platforms for The Church of Pentecost, running on Azure in the UK.", "",
            f"Contact: {EMAIL} · {PHONE_DISPLAY} · {LINKEDIN}", "",
            "## Services", ""]
    llms += [f"- [{x['name']}]({SITE}/services/{x['slug']}/): {x['short']}" for x in SERVICES]
    llms += ["", "## Products", "",
             f"- [CodeGate]({SITE}/products/#codegate): Online coding assessment. Candidates solve problems in a timed browser editor; hidden tests decide correctness and AI grades edge cases, code quality and efficiency. In use, early access.",
             f"- [Mandate]({SITE}/products/#mandate): A safe gateway between AI agents and business systems such as ERP, SQL databases and in-house apps, with permissions, approvals and an audit log. In development.",
             "", "## Case studies", ""]
    llms += [f"- [{x['title']}]({SITE}/case-studies/{x['slug']}/): {x['oneliner']} ({x['headline'][0]} {x['headline'][1].lower()})" for x in CASES]
    llms += ["", "## Company", "",
             f"- [About and contact]({SITE}/#about)",
             f"- [Careers]({SITE}/careers.html): Remote Full Stack Development internship and full-time engineering roles.",
             f"- [All case studies]({SITE}/case-studies/)", ""]
    write("llms.txt", "\n".join(llms))

REMOVED = ["erp-inventory-module", "payment-gateway-integration", "accounting-software-integration",
           "clinic-management-enhancement", "learning-platform-features", "delivery-management-system"]

def redirects():
    """Old case-study URLs that no longer exist: send visitors and crawlers to the case studies page."""
    for slug in REMOVED:
        write(f"case-studies/{slug}/index.html", f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Moved | Altherix</title><meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}/case-studies/"><meta http-equiv="refresh" content="0; url=/case-studies/">
</head><body><p><a href="/case-studies/">See our case studies</a></p></body></html>
''')

if __name__ == "__main__":
    home(); cases_index()
    for c in CASES: case_page(c)
    for s in SERVICES: service_page(s)
    products(); careers(); notfound(); redirects(); seo_files()
    print(f"Built {len(PAGES)} pages + 404, sitemap.xml, robots.txt, llms.txt")
