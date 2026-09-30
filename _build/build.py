#!/usr/bin/env python3
"""Static site generator for altherix.in.
Run from the repo root:  python3 _build/build.py
Writes plain HTML files; GitHub Pages serves them as-is (Jekyll ignores _build/)."""
import json, os, sys
from html import escape as E
sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = []  # for sitemap
V = "3"  # asset cache-buster

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

def url_for(path):
    p = path.replace("index.html", "")
    return SITE + "/" + p

# ── shared chrome ────────────────────────────────────────────────────────────
NAV = [("Services", "/#services", "services"), ("Solutions", "/#solutions", "solutions"),
       ("Case Studies", "/case-studies/", "case-studies"), ("Industries", "/#industries", "industries"),
       ("About", "/#about", "about"), ("Careers", "/careers.html", "careers")]

def head(title, desc, path, jsonld=None, og_type="website"):
    u = url_for(path)
    ld = "".join(f'\n<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    return f"""<!DOCTYPE html>
<html lang="en-IN" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{u}">
<meta name="theme-color" content="#020D34">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{u}">
<meta property="og:site_name" content="Altherix">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="icon" href="/assets/icon-32.png" sizes="32x32" type="image/png">
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
    <a class="brand" href="/" aria-label="Altherix home"><img src="/assets/icon-96.webp" width="34" height="34" alt="">ALTHERIX</a>
    <nav aria-label="Main"><ul class="nav-links">{links}</ul></nav>
    <a class="btn btn-p nav-cta" href="/#contact">Talk to an Engineer</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  {mlinks}
  <a class="btn btn-p" href="/#contact">Talk to an Engineer <span class="arr">→</span></a>
  <div class="mm-meta"><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a></div>
</div>
"""

def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    svc += '<li><a href="/services/enterprise-integration/#cloud">Cloud &amp; DevOps</a></li>'
    ind = "".join(f'<li><a href="/#industries">{n}</a></li>' for n in ["Manufacturing", "Financial Services", "Healthcare", "Education", "Logistics", "Enterprise"])
    return f"""<footer class="foot">
  <div class="ct">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="brand" href="/"><img src="/assets/icon-96.webp" width="34" height="34" alt="" loading="lazy">ALTHERIX</a>
        <p class="foot-tag">Modern Software.<br>Intelligent Systems.<br>Real Business Value.</p>
        <p class="foot-sub">Transforming Software, Amplifying Value.</p>
      </div>
      <div><h2>Services</h2><ul>{svc}</ul></div>
      <div><h2>Industries</h2><ul>{ind}</ul></div>
      <div><h2>Company</h2><ul><li><a href="/#about">About</a></li><li><a href="/case-studies/">Case Studies</a></li><li><a href="/#team">Team</a></li><li><a href="/careers.html">Careers</a></li><li><a href="/#contact">Contact</a></li></ul></div>
      <div><h2>Contact</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li><li><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a></li><li><a href="/#contact">Ooty · India</a></li></ul></div>
    </div>
    <div class="foot-bot">
      <span>© <span data-year>2026</span> Altherix Solutions</span>
      <span>Ooty · India &nbsp;·&nbsp; <a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a></span>
    </div>
  </div>
</footer>
</body>
</html>
"""

def chips(items):
    return '<div class="chips">' + "".join(f'<span class="chip">{E(t)}</span>' for t in items) + "</div>"

ORG = {
  "@context": "https://schema.org", "@type": "Organization", "name": "Altherix Solutions",
  "alternateName": "Altherix", "url": SITE + "/", "logo": SITE + "/assets/icon-512.png",
  "slogan": "Transforming Software, Amplifying Value.",
  "email": EMAIL, "telephone": "+91-8152923515", "sameAs": [LINKEDIN],
  "address": {"@type": "PostalAddress", "streetAddress": "1247 N1, LN Gardens, Stanley Park, Ottupattarai",
              "addressLocality": "Coonoor", "addressRegion": "Tamil Nadu", "postalCode": "643105", "addressCountry": "IN"},
}

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

# ── hero system visual (static SVG, CSS-animated) ────────────────────────────
def hero_svg():
    W, H = 600, 552
    tiers = [("Experience", 60, [170, 283, 396, 510]),
             ("Apps", 170, [215, 340, 465]),
             ("APIs · AI", 280, [160, 260, 360, 460, 560]),
             ("Data", 390, [215, 340, 465]),
             ("Cloud", 490, [280, 400])]
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="viz-t"><title id="viz-t">Layered system diagram: experience, applications, APIs and AI, data and enterprise systems, and cloud infrastructure, connected by flowing data.</title>',
           '<defs><linearGradient id="flowGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9A22B9"/><stop offset=".5" stop-color="#DF3AD2"/><stop offset="1" stop-color="#FA70A5"/></linearGradient>'
           '<radialGradient id="coreGrad"><stop offset="0" stop-color="#FA70A5"/><stop offset=".55" stop-color="#DF3AD2"/><stop offset="1" stop-color="#5D1EA6"/></radialGradient></defs>']
    for name, y, xs in tiers:
        out.append(f'<rect class="viz-tier" x="120" y="{y-26}" width="470" height="52" rx="12"/>')
        out.append(f'<text class="viz-label" x="0" y="{y+4}">{E(name)}</text>')
    paths = []
    for a in range(len(tiers) - 1):
        _, y1, xs1 = tiers[a]; _, y2, xs2 = tiers[a + 1]
        for i, x1 in enumerate(xs1):
            for j, x2 in enumerate(xs2):
                if abs((i / max(1, len(xs1)-1)) - (j / max(1, len(xs2)-1))) <= 0.42:
                    my = (y1 + y2) / 2
                    paths.append(f"M{x1} {y1+9} C{x1} {my} {x2} {my} {x2} {y2-9}")
    for p in paths:
        out.append(f'<path class="viz-line" d="{p}"/>')
    for k, p in enumerate(paths):
        if k % 2 == 0:
            out.append(f'<path class="viz-flow" d="{p}" style="animation-delay:-{(k*0.37)%5.5:.2f}s"/>')
    for ti, (name, y, xs) in enumerate(tiers):
        for i, x in enumerate(xs):
            core = (ti == 2 and i == 2)
            if core:
                out.append(f'<circle class="viz-ring" cx="{x}" cy="{y}" r="14"/>')
                out.append(f'<circle class="viz-node core" cx="{x}" cy="{y}" r="11"/>')
            else:
                out.append(f'<circle class="viz-node" cx="{x}" cy="{y}" r="8"/>')
                out.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{"#FA70A5" if (i+ti)%3==0 else "#9A22B9"}"/>')
    out.append("</svg>")
    return "\n".join(out)

GLYPHS = {
  "software-engineering": '<svg class="cap-glyph" viewBox="0 0 64 64" fill="none" stroke="url(#g1)" stroke-width="1.5" aria-hidden="true"><defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9A22B9"/><stop offset="1" stop-color="#FA70A5"/></linearGradient></defs><rect x="6" y="10" width="52" height="36" rx="5"/><path d="M6 18h52"/><path d="M22 28l-6 5 6 5M42 28l6 5-6 5M34 25l-4 16"/><path d="M24 54h16M32 46v8"/></svg>',
  "modernization": '<svg class="cap-glyph" viewBox="0 0 64 64" fill="none" stroke="url(#g2)" stroke-width="1.5" aria-hidden="true"><defs><linearGradient id="g2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9A22B9"/><stop offset="1" stop-color="#FA70A5"/></linearGradient></defs><rect x="6" y="34" width="20" height="20" rx="3" stroke-dasharray="3 3"/><rect x="38" y="10" width="20" height="20" rx="3"/><path d="M26 44c10 0 12-24 12-24"/><path d="M33 22l5-4 3 6"/><circle cx="16" cy="44" r="3"/><circle cx="48" cy="20" r="3"/></svg>',
  "ai-automation": '<svg class="cap-glyph" viewBox="0 0 64 64" fill="none" stroke="url(#g3)" stroke-width="1.5" aria-hidden="true"><defs><linearGradient id="g3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9A22B9"/><stop offset="1" stop-color="#FA70A5"/></linearGradient></defs><circle cx="12" cy="32" r="5"/><circle cx="32" cy="14" r="5"/><circle cx="32" cy="50" r="5"/><circle cx="52" cy="32" r="5"/><path d="M16 29l12-11M16 35l12 11M36 18l12 11M36 46l12-11M32 19v26"/><circle cx="32" cy="32" r="2"/></svg>',
  "enterprise-integration": '<svg class="cap-glyph" viewBox="0 0 64 64" fill="none" stroke="url(#g4)" stroke-width="1.5" aria-hidden="true"><defs><linearGradient id="g4" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9A22B9"/><stop offset="1" stop-color="#FA70A5"/></linearGradient></defs><rect x="4" y="8" width="18" height="14" rx="3"/><rect x="4" y="42" width="18" height="14" rx="3"/><rect x="42" y="25" width="18" height="14" rx="3"/><path d="M22 15h8v34h-8M30 32h12"/><circle cx="30" cy="32" r="2.5"/></svg>',
}

def cs_panel(c, big=True):
    h = c["headline"]
    subs = "".join(f"<div><b>{E(v)}</b>{E(l)}</div>" for v, l in c["metrics"][1:3] if v != "Live")
    live = '<span class="cs-live">Live in production</span>' if c.get("featured") else ""
    client = f'<p class="cs-client">{E(c["client"])}</p>' if c.get("client") else ""
    return f"""<article class="cs rv{' cs-feature' if c.get('featured') else ''}">
  <div class="cs-metric">
    <div><div class="cs-big">{E(h[0])}</div><div class="cs-big-l">{E(h[1])}</div></div>
    <div class="cs-sub">{subs}</div>
  </div>
  <div class="cs-body">
    <div class="cs-cat">{E(c['category'])}</div>
    <h3>{E(c['title'])}</h3>{client}
    <div class="cs-ps"><div><h4>Problem</h4><p>{E(c['problem'])}</p></div><div><h4>Solution</h4><p>{E(c['solution'])}</p></div></div>
    {chips(c['tech'][:7])}
    <div class="cs-foot">{live}<a class="link" href="/case-studies/{c['slug']}/">Read case study <span aria-hidden="true">→</span></a></div>
  </div>
</article>"""

def contact_section(heading="Have a difficult software problem?", lede="Whether you're modernizing a legacy platform, integrating enterprise systems, or figuring out where AI actually fits, start with a conversation with our engineering team."):
    opts = "".join(f"<option>{s['name']}</option>" for s in SERVICES) + "<option>Cloud &amp; DevOps</option><option>Not sure yet</option>"
    return f"""<section class="sec cta" id="contact" aria-labelledby="contact-h">
  <div class="ct cta-grid">
    <div class="rv">
      <div class="kicker">Talk to an engineer</div>
      <h2 class="h2" id="contact-h">{heading}</h2>
      <p class="lede">{lede}</p>
      <div class="contact-list">
        <a href="mailto:{EMAIL}"><span>Email</span><b>{EMAIL}</b></a>
        <a href="tel:{PHONE_TEL}"><span>Phone</span><b>{PHONE_DISPLAY}</b></a>
        <a href="{LINKEDIN}" target="_blank" rel="noopener"><span>LinkedIn</span><b>linkedin.com/company/altherix</b></a>
        <div><span>Office</span><b>{'<br>'.join(ADDRESS)}</b></div>
      </div>
    </div>
    <form class="form rv" id="contact-form" novalidate>
      <div class="row">
        <div><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
        <div><label for="f-email">Work email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      </div>
      <div class="row">
        <div><label for="f-company">Company</label><input id="f-company" name="company" autocomplete="organization"></div>
        <div><label for="f-topic">Area</label><select id="f-topic" name="topic"><option value="">Choose one…</option>{opts}</select></div>
      </div>
      <div><label for="f-msg">What are you working on?</label><textarea id="f-msg" name="message" required placeholder="The system, the problem, and what a good outcome looks like."></textarea></div>
      <button class="btn btn-p" type="submit">Talk to an Engineer <span class="arr">→</span></button>
      <p class="form-note">Opens your email app with the message addressed to {EMAIL}.</p>
      <p class="form-ok" id="form-ok" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>"""

# ── HOME ─────────────────────────────────────────────────────────────────────
def home():
    path = "index.html"
    outcomes = [("85%", "Less manual work", "ERP inventory module", "erp-inventory-module"),
                ("90%", "Time saved", "Accounting integration", "accounting-software-integration"),
                ("70%", "Fewer no-shows", "Clinic management", "clinic-management-enhancement"),
                ("35%", "Higher conversions", "Payment integration", "payment-gateway-integration"),
                ("40%", "Faster deliveries", "Delivery management", "delivery-management-system"),
                ("8K+", "Active students", "Learning platform", "learning-platform-features"),
                ("3K+", "Patients / month", "Across four clinics", "clinic-management-enhancement"),
                ("7", "Hierarchy levels", "Global reporting system", "missions-office-enterprise-system")]
    out_html = "".join(f'<a class="outcome" href="/case-studies/{s}/"><span class="n">{n}</span><span class="l">{l}</span><span class="s">{d}</span></a>' for n, l, d, s in outcomes)

    caps = ""
    for s in SERVICES:
        caps += f"""<article class="cap rv">
  <div class="cap-top"><span class="cap-n">{s['n']}</span>{GLYPHS[s['slug']]}</div>
  <h3>{s['name']}</h3>
  <p>{E(s['short'])}</p>
  <ul class="cap-list">{''.join(f'<li>{E(x)}</li>' for x in s['list'])}</ul>
  {chips(s['tech'][:6])}
  <a class="link" href="/services/{s['slug']}/">Learn more <span aria-hidden="true">→</span></a>
</article>"""
    caps += """<div class="cap-extra rv"><div><strong>Cloud &amp; DevOps</strong><p>CI/CD on Azure DevOps and GitHub Actions, hardened Azure infrastructure, and monitoring that catches problems before users do — part of every engagement, and available on its own.</p></div><a class="link" href="/services/enterprise-integration/#cloud">Cloud &amp; DevOps <span aria-hidden="true">→</span></a></div>"""

    featured = [CASE[s] for s in ["church-management-system", "missions-office-enterprise-system", "erp-inventory-module", "accounting-software-integration", "clinic-management-enhancement"]]
    panels = "\n".join(cs_panel(c) for c in featured)

    ai_areas = [("AI Integration", "Connect AI capabilities to existing business applications."),
                ("AI Agents", "Automate multi-step workflows with appropriate human oversight."),
                ("Intelligent Automation", "Turn repetitive operational processes into adaptive workflows."),
                ("Enterprise AI", "Build secure, governed AI experiences around business data.")]
    ai_html = "".join(f'<div class="ai-area rv"><span class="i">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(ai_areas))

    layers = [("Experience", "Web, mobile and dashboards", ["React", "TypeScript", "Angular", "React Native", "Alpine.js", "Chart.js"]),
              ("Applications", "Domain logic and workflows", [".NET 9", "ASP.NET Core", "Spring Boot", "Laravel", "Django", "Node.js"]),
              ("APIs · Services · AI", "Contracts between systems", ["REST", "SignalR", "Hangfire", "LLM integration", "Payment & messaging APIs"]),
              ("Data & Enterprise", "Records, reporting and ERP", ["SQL Server", "MySQL", "PostgreSQL", "MongoDB", "SAP", "Tally · Zoho Books"]),
              ("Cloud · DevOps", "Infrastructure, release, observability", ["Azure App Service", "Azure SQL", "Blob Storage", "AWS S3", "Azure DevOps", "GitHub Actions"])]
    stack = ""
    for i, (n, sub, t) in enumerate(layers):
        if i: stack += '<div class="link-v" aria-hidden="true"><i></i><i></i><i></i></div>'
        stack += f'<div class="layer rv"><div class="layer-n"><span class="idx">L{i+1}</span><div><b>{n}</b><div style="font-size:.8rem;color:var(--ink-3)">{sub}</div></div></div>{chips(t)}</div>'

    inds = ""
    for i, (n, d, slugs) in enumerate(INDUSTRIES):
        links = " · ".join(f'<a href="/case-studies/{s}/">{E(CASE[s]["title"])} →</a>' for s in slugs[:1])
        inds += f'<div class="ind rv"><h3>{n}<small>{len(slugs)} case stud{"ies" if len(slugs)>1 else "y"}</small></h3><p>{d}</p>{links}</div>'

    principles = [("We improve before we replace.", "Existing systems often contain years of business knowledge. We modernize intelligently instead of rewriting everything unnecessarily."),
                  ("Engineers stay close to the problem.", "Architecture, development and delivery remain connected. The people who scope your system are the people who build and support it."),
                  ("Production is the finish line.", "We care about deployment, reliability, observability and real-world operation — not just prototypes."),
                  ("Technology follows the problem.", "We use the right architecture and technology for the problem rather than forcing every project into the same solution — .NET one quarter, Laravel the next.")]
    pr_html = "".join(f'<div class="pr rv"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(principles))

    ico = {
      "Security": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg>',
      "Reliability": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h4l3-7 4 14 3-7h4"/></svg>',
      "Delivery": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="12" r="2.5"/><path d="M6 8.5v7M8.3 7l7.5 4M8.3 17l7.5-4"/></svg>',
      "Governance": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
    }
    practices = [("Security", [("Role-based access", "throughout our production platforms"), ("Scoped queries", "users only retrieve data they are responsible for"), ("Secrets management", "credentials kept out of code and in order")]),
                 ("Reliability", [("Logging & alerting", "for production workloads"), ("Backups", "kept in good order"), ("Background jobs", "scheduled work handled outside the request path")]),
                 ("Delivery", [("CI/CD", "Azure DevOps and GitHub Actions"), ("Gated releases", "production changes go through approval"), ("Code review & tests", "thorough reviews; tests written alongside code")]),
                 ("Governance", [("Audit trails", "recorded across our enterprise platforms"), ("Export provenance", "reports stamped with scope, period and origin"), ("Access control", "enforced at data level, not just in the UI")])]
    prac_html = "".join(f'<div class="rv"><h3>{ico[t]}{t}</h3><ul>{"".join(f"<li><b>{a}</b> — {b}</li>" for a, b in items)}</ul></div>' for t, items in practices)

    team = "".join(f'<div class="member rv"><div class="member-top"><div class="avatar" aria-hidden="true">{ini}</div><div><h3>{n}</h3><div class="member-role">{r}</div></div></div>{chips(ex)}</div>' for n, r, ini, ex in TEAM)

    jsonld = [ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "Altherix", "url": SITE + "/"}]
    html = head("Altherix | Software Engineering, AI & Enterprise Modernization",
                "Altherix engineers modern software, enterprise integrations and production-ready AI systems for businesses that depend on their technology.",
                path, jsonld) + nav() + f"""
<main id="main">

<section class="hero" id="home" aria-labelledby="hero-h">
  <div class="ct">
    <div>
      <div class="kicker rv">Altherix · Engineering from the Nilgiris</div>
      <h1 class="h1 rv" id="hero-h" style="margin-top:1.3rem"><span>Modern Software.</span><span>Intelligent Systems.</span><span><em>Real Business Value.</em></span></h1>
      <p class="lede rv">Altherix engineers, modernizes and intelligently automates the software systems businesses depend on.</p>
      <div class="caps rv"><span>Software Engineering</span><span>Modernization</span><span>AI &amp; Automation</span><span>Enterprise Integration</span></div>
      <div class="hero-btns rv">
        <a class="btn btn-p" href="#contact">Talk to an Engineer <span class="arr">→</span></a>
        <a class="btn btn-o" href="#work">Explore Our Work</a>
      </div>
    </div>
    <div class="hero-viz rv">{hero_svg()}</div>
  </div>
</section>

<section class="proof" aria-label="What we deliver">
  <div class="ct">
    <div class="proof-caps rv"><div>Production systems</div><div>Enterprise engineering</div><div>Cloud &amp; integration</div><div>AI &amp; automation</div></div>
    <div class="outcomes rv">{out_html}</div>
    <p class="proof-note">Outcomes reported on client engagements. Select a figure to read the case study.</p>
  </div>
</section>

<section class="sec" id="services" aria-labelledby="svc-h">
  <div class="ct">
    <div class="sec-hd split">
      <div><div class="kicker rv">What we do</div><h2 class="h2 rv" id="svc-h">Engineering for <em>real&#8209;world complexity.</em></h2></div>
      <p class="lede rv">Four capabilities, one team. The engineers who scope your system are the ones who build it, deploy it and keep it running.</p>
    </div>
    <div class="caps-grid">{caps}</div>
  </div>
</section>

<section class="sec sec-tint" id="work" aria-labelledby="work-h">
  <div class="ct">
    <div class="sec-hd split">
      <div><div class="kicker rv">Featured case studies</div><h2 class="h2 rv" id="work-h">What we've built, and <em>what it changed.</em></h2></div>
      <p class="lede rv">From two production platforms for a global organisation to focused modules that removed most of a team's manual work.</p>
    </div>
    <div class="cs-list">{panels}</div>
    <div class="more-row"><a class="btn btn-o" href="/case-studies/">All {len(CASES)} case studies <span class="arr">→</span></a></div>
  </div>
</section>

<section class="sec ai" id="solutions" aria-labelledby="ai-h">
  <div class="ct ai-grid">
    <div>
      <div class="kicker rv">AI &amp; Automation</div>
      <h2 class="h2 rv" id="ai-h">AI that works <em>in production.</em></h2>
      <p class="ai-quote rv">AI doesn't replace good engineering. It depends on it.</p>
      <div class="ai-when rv">
        <div><b>Use AI</b><span>when the input is unstructured, the judgement is fuzzy, and a person can review what matters.</span></div>
        <div><b>Use software</b><span>when the rules are known. Invoicing, reconciliation and reminders don't need a model — they need solid automation.</span></div>
        <div><b>Either way</b><span>it runs with access control, logging and an owner, like everything else we ship.</span></div>
      </div>
      <a class="link rv" style="margin-top:2rem" href="/services/ai-automation/">How we approach AI &amp; automation <span aria-hidden="true">→</span></a>
    </div>
    <div class="ai-areas">{ai_html}</div>
  </div>
</section>

<section class="sec" id="architecture" aria-labelledby="arch-h">
  <div class="ct arch">
    <div>
      <div class="kicker rv">Architecture</div>
      <h2 class="h2 rv" id="arch-h">Built for <em>production.</em></h2>
      <p class="lede rv">Every system we deliver is designed as a whole — from the screen a user touches down to the pipeline that releases it.</p>
      <div class="arch-notes rv">
        <div><b>Real-time where it matters</b>Live attendance check-in over WebSockets with SignalR.</div>
        <div><b>Work outside the request</b>Scheduled background jobs with Hangfire expand recurring events and keep data current.</div>
        <div><b>Access at the data layer</b>Hierarchy-scoped queries, so users only ever retrieve what they're responsible for.</div>
      </div>
    </div>
    <div class="stack" role="list" aria-label="Architecture layers">{stack}</div>
  </div>
</section>

<section class="sec sec-tint" id="industries" aria-labelledby="ind-h">
  <div class="ct">
    <div class="sec-hd split">
      <div><div class="kicker rv">Industries</div><h2 class="h2 rv" id="ind-h">Engineering across <em>complex domains.</em></h2></div>
      <p class="lede rv">Each of these comes from delivered work, not a target list.</p>
    </div>
    <div class="ind-grid">{inds}</div>
  </div>
</section>

<section class="sec" id="why" aria-labelledby="why-h">
  <div class="ct">
    <div class="sec-hd"><div class="kicker rv">Why Altherix</div><h2 class="h2 rv" id="why-h">Why teams work <em>with Altherix.</em></h2></div>
    <div class="principles">{pr_html}</div>
  </div>
</section>

<section class="sec sec-tint" id="practices" aria-labelledby="prac-h">
  <div class="ct">
    <div class="sec-hd split">
      <div><div class="kicker rv">Engineering practices</div><h2 class="h2 rv" id="prac-h">The unglamorous parts, <em>done properly.</em></h2></div>
      <p class="lede rv">What we build into production systems as a matter of course.</p>
    </div>
    <div class="prac">{prac_html}</div>
  </div>
</section>

<section class="sec" id="team" aria-labelledby="team-h">
  <div class="ct">
    <div class="sec-hd split">
      <div><div class="kicker rv">Team</div><h2 class="h2 rv" id="team-h">People behind <em>the systems.</em></h2></div>
      <p class="team-statement rv">Built by engineers who have spent years solving real software problems.</p>
    </div>
    <div class="team">{team}</div>
  </div>
</section>

<section class="sec sec-tint" id="about" aria-labelledby="about-h">
  <div class="ct story">
    <div>
      <div class="kicker rv">Our story</div>
      <h2 class="h2 rv" id="about-h">Global engineering. <em>Rooted in the Nilgiris.</em></h2>
      <p class="rv">Altherix was founded in Ooty, high in the Nilgiris. It is an unusual place to build an engineering company — and a deliberate one. A small, senior team, away from the churn of a large delivery centre, with the focus to do careful work.</p>
      <p class="rv">Our work isn't bound by our postcode. Platforms we've built run in production on Azure in the UK for a global organisation, alongside systems for manufacturers, clinics, ed-tech, logistics and finance teams in India.</p>
      <p class="rv">What hasn't changed since the start: the conviction that your existing software is the backbone of your business, and that it usually deserves improving before it deserves replacing.</p>
    </div>
    <div class="story-geo rv" aria-hidden="true">
      <svg viewBox="0 0 520 300"><defs><linearGradient id="arc" x1="0" x2="1"><stop offset="0" stop-color="#FA70A5"/><stop offset="1" stop-color="#9A22B9"/></linearGradient></defs>
        <g fill="rgba(246,244,244,.14)">{''.join(f'<circle cx="{x}" cy="{y}" r="1.4"/>' for x in range(20, 520, 16) for y in range(20, 300, 16) if ((x*7+y*3) % 11) < 6)}</g>
        <path d="M380 210 C 320 40, 200 30, 150 90" fill="none" stroke="url(#arc)" stroke-width="1.6" class="viz-flow" style="stroke-dasharray:4 8;animation-duration:12s"/>
        <path d="M380 210 C 360 160, 330 150, 300 180" fill="none" stroke="url(#arc)" stroke-width="1.2" opacity=".7"/>
        <circle cx="380" cy="210" r="6" fill="#DF3AD2"/><circle class="viz-ring" cx="380" cy="210" r="8"/>
        <circle cx="150" cy="90" r="4.5" fill="#F6F4F4"/><circle cx="300" cy="180" r="3.5" fill="#F6F4F4" opacity=".8"/>
        <text class="viz-label" x="392" y="232">Ooty · Nilgiris</text><text class="viz-label" x="96" y="76">UK · Azure UK South</text><text class="viz-label" x="232" y="202">India</text>
      </svg>
      <div class="geo-legend"><div><b>Founded in Ooty</b>Office in Coonoor, Nilgiris</div><div><b>Delivering beyond</b>Production platforms in India and the UK</div></div>
    </div>
  </div>
</section>

{contact_section()}

</main>
""" + footer()
    write(path, html); PAGES.append((path, "1.0"))

# ── CASE STUDIES INDEX ───────────────────────────────────────────────────────
def cases_index():
    path = "case-studies/index.html"
    panels = "\n".join(cs_panel(c) for c in CASES)
    html = head("Case Studies | Altherix", "Production systems Altherix has designed, built and integrated — with the problems, the engineering and the measurable outcomes.", path,
                [ORG, crumbs_ld([("Home", "/"), ("Case Studies", "/case-studies/")])]) + nav("case-studies") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Case Studies</nav>
  <div class="kicker">Case studies</div>
  <h1>Production systems, <em class="grad-text">measurable outcomes.</em></h1>
  <p class="lede">{len(CASES)} engagements across nonprofit, manufacturing, finance, healthcare, education and logistics. Each one shows the problem, the engineering and what changed.</p>
</div></header>
<section class="sec"><div class="ct"><div class="cs-list">{panels}</div></div></section>
{contact_section("Discuss a similar problem.", "Tell us about the system you're working with and what a good outcome looks like. You'll hear back from an engineer.")}
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.9"))

# ── CASE STUDY PAGE ──────────────────────────────────────────────────────────
def case_page(c):
    path = f"case-studies/{c['slug']}/index.html"
    svc = SERVICE[c["related_service"]]
    toc = [("summary", "Executive summary"), ("challenge", "The challenge"), ("approach", "The approach"), ("architecture", "Architecture"),
           ("engineering", "Engineering"), ("technology", "Technology"), ("results", "Results"), ("impact", "Impact")]
    related = [x for x in CASES if x["slug"] != c["slug"] and (x["industry"] == c["industry"] or x["related_service"] == c["related_service"])][:2]
    rel_html = "".join(f'<a class="card" href="/case-studies/{r["slug"]}/"><span class="cs-cat">{E(r["category"])}</span><span class="n">{r["headline"][0]}<small>{E(r["headline"][1])}</small></span><h3>{E(r["title"])}</h3><p>{E(r["oneliner"])}</p></a>' for r in related)
    facts = [("Category", c["category"]), ("Industry", c["industry"])]
    if c.get("client"): facts.insert(0, ("Client", c["client"]))
    if c.get("featured"): facts.append(("Status", "Live in production"))
    jsonld = [ORG, crumbs_ld([("Home", "/"), ("Case Studies", "/case-studies/"), (c["title"], f"/case-studies/{c['slug']}/")]),
              {"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "description": c["oneliner"],
               "author": {"@type": "Organization", "name": "Altherix Solutions"}, "publisher": {"@type": "Organization", "name": "Altherix Solutions", "logo": {"@type": "ImageObject", "url": SITE + "/assets/icon-512.png"}},
               "image": SITE + "/assets/og.png", "mainEntityOfPage": url_for(path)}]
    html = head(f"{c['title']} — Case Study | Altherix", c["oneliner"], path, jsonld, "article") + nav("case-studies") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/case-studies/">Case Studies</a> / {E(c['title'])}</nav>
  <div class="kicker">{E(c['category'])}</div>
  <h1>{E(c['title'])}</h1>
  <p class="lede">{E(c['oneliner'])}</p>
  <div class="facts">{''.join(f'<div><span>{k}</span><b>{E(v)}</b></div>' for k, v in facts)}</div>
</div></header>
<section class="sec"><div class="ct article">
  <nav class="toc" aria-label="On this page">{''.join(f'<a href="#{i}">{t}</a>' for i, t in toc)}</nav>
  <div>
    <div class="block" id="summary"><h2>Executive summary</h2><p>{E(c['summary'])}</p></div>
    <div class="block" id="challenge"><h2>The challenge</h2>{''.join(f'<p>{E(p)}</p>' for p in c['challenge'])}</div>
    <div class="block" id="approach"><h2>The approach</h2><ul class="ticks">{''.join(f'<li><span><b>{E(a)}.</b> {E(b)}</span></li>' for a, b in c['approach'])}</ul></div>
    <div class="block" id="architecture"><h2>Architecture</h2><div class="arch-mini">{''.join(f'<div><span>{E(a)}</span><p>{E(b)}</p></div>' for a, b in c['architecture'])}</div></div>
    <div class="block" id="engineering"><h2>Engineering</h2><ul class="ticks">{''.join(f'<li><span><b>{E(a)}</b> — {E(b)}</span></li>' for a, b in c['engineering'])}</ul></div>
    <div class="block" id="technology"><h2>Technology</h2>{chips(c['tech'])}</div>
    <div class="block" id="results"><h2>Results</h2><h3 style="font-family:var(--mono);font-size:.7rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);margin-bottom:.8rem">Key metrics</h3><div class="metrics">{''.join(f'<div><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in c['metrics'])}</div></div>
    <div class="block" id="impact"><h2>Impact</h2><p>{E(c['impact'])}</p><p><a class="link" href="/services/{svc['slug']}/">Related service: {svc['name']} <span aria-hidden="true">→</span></a></p></div>
  </div>
</div></section>
{f'<section class="sec sec-tint"><div class="ct"><div class="sec-hd"><div class="kicker">More work</div><h2 class="h2" style="font-size:clamp(1.7rem,3vw,2.4rem)">Related case studies</h2></div><div class="cards">{rel_html}</div></div></section>' if rel_html else ''}
{contact_section("Discuss a similar problem.", "If this looks like something you're dealing with, tell us about your system. You'll hear back from an engineer.")}
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.8"))

# ── SERVICE PAGE ─────────────────────────────────────────────────────────────
def service_page(s):
    path = f"services/{s['slug']}/index.html"
    cases = "".join(f'<a class="card" href="/case-studies/{x}/"><span class="cs-cat">{E(CASE[x]["category"])}</span><span class="n">{CASE[x]["headline"][0]}<small>{E(CASE[x]["headline"][1])}</small></span><h3>{E(CASE[x]["title"])}</h3><p>{E(CASE[x]["oneliner"])}</p></a>' for x in s["cases"])
    cloud = ""
    if s.get("cloud"):
        cl = s["cloud"]
        cloud = f'<section class="sec" id="cloud"><div class="ct"><div class="sec-hd split"><div><div class="kicker">Also</div><h2 class="h2">{cl["title"]}</h2></div><p class="lede">{E(cl["text"])}</p></div><div class="svc-cap">{"".join(f"<div><h3>{E(x)}</h3></div>" for x in cl["list"])}</div></div></section>'
    others = "".join(f'<a class="card" href="/services/{o["slug"]}/"><span class="cs-cat">{o["n"]}</span><h3>{o["name"]}</h3><p>{E(o["short"])}</p></a>' for o in SERVICES if o["slug"] != s["slug"])
    desc = s["short"]
    jsonld = [ORG, crumbs_ld([("Home", "/"), ("Services", "/#services"), (s["name"], f"/services/{s['slug']}/")]),
              {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": desc, "provider": {"@type": "Organization", "name": "Altherix Solutions", "url": SITE + "/"}, "areaServed": "Worldwide"}]
    html = head(f"{s['name']} | Altherix", desc, path, jsonld) + nav("services") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/#services">Services</a> / {s['name']}</nav>
  <div class="kicker">{s['n']} · {s['name']}</div>
  <h1>{s['h1'].replace('<em>', '<em class="grad-text" style="font-style:normal">')}</h1>
  <p class="lede">{E(s['lede'])}</p>
  <div class="hero-btns"><a class="btn btn-p" href="#contact">Talk to an Engineer <span class="arr">→</span></a><a class="btn btn-o" href="#work">Relevant work</a></div>
</div></header>
<section class="sec"><div class="ct article" style="grid-template-columns:1fr">
  <div class="block"><div class="kicker">The problem</div><h2 style="margin-top:1rem">Why this is harder than it looks</h2>{''.join(f'<p>{E(p)}</p>' for p in s['problem'])}</div>
  <div class="block"><div class="kicker">How we approach it</div><h2 style="margin-top:1rem">Our approach</h2><ol class="steps">{''.join(f'<li><span><b>{E(a)}</b>{E(b)}</span></li>' for a, b in s['approach'])}</ol></div>
  <div class="block"><div class="kicker">Capabilities</div><h2 style="margin-top:1rem">What we do</h2><div class="svc-cap">{''.join(f'<div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in s['caps'])}</div></div>
  <div class="block"><div class="kicker">Technology</div><h2 style="margin-top:1rem">What we work with</h2>{chips(s['tech'])}</div>
</div></section>
{cloud}
<section class="sec sec-tint" id="work"><div class="ct">
  <div class="sec-hd split"><div><div class="kicker">Relevant case studies</div><h2 class="h2" style="font-size:clamp(1.8rem,3.4vw,2.6rem)">{s.get('cases_title', 'Where we have done this')}</h2></div>{f'<p class="lede">{E(s["cases_note"])}</p>' if s.get('cases_note') else ''}</div>
  <div class="cards">{cases}</div>
</div></section>
<section class="sec"><div class="ct"><div class="sec-hd"><div class="kicker">Other capabilities</div></div><div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{others}</div></div></section>
{contact_section()}
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.8"))

# ── CAREERS ──────────────────────────────────────────────────────────────────
def careers():
    path = "careers.html"
    def apply(subject, body):
        from urllib.parse import quote
        return f'mailto:{EMAIL}?subject={quote(subject)}&amp;body={quote(body)}'
    std_body = "Hello Altherix team,\n\nI'd like to apply for the {r} role.\n\nA little about me:\n\n\nLinks (GitHub / portfolio / LinkedIn):\n\n\nMy CV is attached.\n\nThank you,"
    roles = [
      dict(t="Full Stack Development Intern", new=True, facts=["Fully remote", "2 or 3 months", "Stipend provided", "Paid 3-day onsite in Ooty"],
           about="A fully remote internship of two or three months, with a stipend. You'll work on real client projects from week one, with a senior engineer as your mentor. Our team is based in Coonoor, near Ooty, and interns join us for a paid three-day onsite in Ooty.",
           do=["Ship features into a live codebase under close review", "Write tests and documentation alongside your code", "Learn how professional delivery runs, from estimate to release"],
           want=["Fluency in at least one language — C#, Java, PHP, Python or JavaScript", "Something you've built that you can walk us through, however small", "Preferred: BSc or BCA with a Computer Science major"],
           nice=None, how=f"Send your CV and a link to your work to {EMAIL} with the subject “Full Stack Internship”.",
           href=apply("Full Stack Internship", "Hello Altherix team,\n\nI'd like to apply for the Full Stack Development Internship.\n\nA little about me:\n\n\nLink to my work:\n\n\nMy CV is attached.\n\nThank you,"), open=True),
      dict(t="Senior Full-Stack Engineer — .NET & React", facts=["Ooty · Hybrid", "Full time", "5+ years"],
           about="You'll lead delivery on enterprise platforms built with ASP.NET Core and React — designing the data model, building the API, shaping the front end, and taking it through to an Azure deployment. This is our most senior individual-contributor track.",
           do=["Design and build REST APIs with ASP.NET Core and Entity Framework Core", "Build front ends in React and TypeScript with a considered component architecture", "Model relational schemas and write queries that stay fast as data grows", "Work directly with clients to turn ambiguous requirements into a shippable scope", "Review other engineers' work and raise the standard of the codebase"],
           want=["Five or more years building and shipping production web applications", "Strong C# and .NET, with real Entity Framework and SQL Server experience", "Confident in React, TypeScript and modern front-end tooling", "Comfortable owning a deployment — CI/CD pipelines, cloud hosting, diagnosing production issues", "Clear written and spoken communication; you'll be in front of clients"],
           nice=["Azure services — App Service, SQL, Blob Storage, DevOps pipelines", "Background jobs and real-time messaging (Hangfire, SignalR or equivalents)", "Experience modernising a legacy codebase without a rewrite"],
           href=apply("Application — Senior Full-Stack Engineer (.NET & React)", std_body.format(r="Senior Full-Stack Engineer"))),
      dict(t="Full-Stack Engineer — PHP / Laravel", facts=["Ooty · Hybrid", "Full time", "2–5 years"],
           about="We build reporting and operational platforms on Laravel for clients who need a lot of domain logic handled correctly. You'll work across the stack — schema, application logic, and the dashboards people actually look at every day.",
           do=["Build features across Laravel applications — migrations, models, services, controllers and Blade views", "Write aggregation and reporting logic where correctness genuinely matters", "Build interactive dashboards and data visualisations for non-technical users", "Implement role-based access control and audit trails", "Write tests that give us confidence to deploy on a Friday"],
           want=["Two or more years with PHP and a modern framework, ideally Laravel", "Solid relational database skills — you can read a slow query and fix it", "Working knowledge of JavaScript and at least one front-end approach", "Care about data accuracy and edge cases, not just the happy path"],
           nice=["Charting libraries, PDF and spreadsheet generation", "Experience with multi-tenant or hierarchical permission models"],
           href=apply("Application — Full-Stack Engineer (PHP / Laravel)", std_body.format(r="Full-Stack Engineer (Laravel)"))),
      dict(t="Cloud & DevOps Engineer", facts=["Ooty · Hybrid", "Full time", "3+ years"],
           about="You'll own how our clients' systems get built, released and observed — pipelines, environments, cost, and the alerting that tells us something is wrong before the client does.",
           do=["Build and maintain CI/CD pipelines across Azure DevOps and GitHub Actions", "Provision and harden cloud infrastructure, primarily on Azure", "Set up monitoring, logging and alerting for production workloads", "Lead migrations from on-premise or shared hosting into the cloud", "Keep secrets, backups and access controls in good order"],
           want=["Three or more years in a DevOps, platform or SRE role", "Hands-on Azure experience; AWS or GCP also considered", "Comfortable scripting in Bash, PowerShell or Python", "Containers and infrastructure-as-code in day-to-day use"],
           nice=None, href=apply("Application — Cloud & DevOps Engineer", std_body.format(r="Cloud & DevOps Engineer"))),
    ]
    def ul(x): return "<ul>" + "".join(f"<li>{E(i)}</li>" for i in x) + "</ul>"
    rhtml = ""
    for r in roles:
        rhtml += f"""<details class="role rv"{' open' if r.get('open') else ''}>
  <summary><div><div class="role-t">{E(r['t'])}{'<span class="role-new">Now hiring</span>' if r.get('new') else ''}</div>{chips(r['facts'])}</div><span class="role-chev" aria-hidden="true">+</span></summary>
  <div class="role-body">
    <h4>About the role</h4><p>{E(r['about'])}</p>
    <h4>What you'll do</h4>{ul(r['do'])}
    <h4>What we're looking for</h4>{ul(r['want'])}
    {'<h4>Nice to have</h4>' + ul(r['nice']) if r.get('nice') else ''}
    {'<h4>How to apply</h4><p>' + E(r['how']) + '</p>' if r.get('how') else ''}
    <a class="btn btn-p" href="{r['href']}">Apply for this role <span class="arr">→</span></a>
  </div>
</details>"""
    why = [("You own the whole problem", "Engineers here talk to clients, shape the solution, build it and see it through to deployment. No handing a spec down a chain and hoping."),
           ("Real systems, real users", "The platforms we build run production workloads for organisations that depend on them. Your code is used, not shelved."),
           ("Breadth by design", "Consulting means variety — .NET one quarter, Laravel the next, an Azure migration after that."),
           ("Senior people to learn from", "A deliberately small team with deep enterprise and architecture experience. Reviews are thorough and mentoring is direct.")]
    steps = [("Application", "Send your CV and a few lines about what you've built. We read every one and reply within a week."),
             ("Intro call", "Thirty minutes with an engineer. Your background, our work, and whether the fit makes sense both ways."),
             ("Technical conversation", "We walk through a realistic problem together and discuss code you've written. No whiteboard algorithms, no unpaid take-home projects."),
             ("Offer", "A final conversation on scope, expectations and compensation, then a written offer.")]
    bene = [("Paid intern onsite", "Interns join the team for a paid three-day onsite in Ooty — time to meet your mentor and the people you've been shipping with.", True),
            ("Hybrid working", "Full-time roles split between our Nilgiris office and home, arranged around delivery rather than a fixed rota.", False),
            ("Learning budget", "An annual allowance for certifications, courses and conferences, plus time to use it.", False),
            ("Health cover", "Medical insurance for you and your immediate family.", False),
            ("Client-facing exposure", "You sit in the room where decisions are made — experience that's hard to get in a large delivery centre.", False),
            ("Sane delivery", "We estimate honestly and push back on unrealistic dates. Crunch is a planning failure, not a culture.", False)]
    jobs = [{"@context": "https://schema.org", "@type": "JobPosting", "title": "Full Stack Development Intern",
             "description": roles[0]["about"], "employmentType": "INTERN", "datePosted": "2026-09-30",
             "hiringOrganization": {"@type": "Organization", "name": "Altherix Solutions", "sameAs": LINKEDIN, "logo": SITE + "/assets/icon-512.png"},
             "jobLocationType": "TELECOMMUTE", "applicantLocationRequirements": {"@type": "Country", "name": "India"},
             "educationRequirements": "BSc / BCA with a Computer Science major preferred"}]
    html = head("Careers | Altherix", "Join Altherix — a senior engineering team in the Nilgiris building production systems. Open roles, including a fully remote Full Stack Development internship.", path,
                [ORG, crumbs_ld([("Home", "/"), ("Careers", "/careers.html")])] + jobs) + nav("careers") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Careers</nav>
  <div class="kicker">Careers at Altherix</div>
  <h1>Small team. <em class="grad-text" style="font-style:normal">Serious systems.</em></h1>
  <p class="lede">Our work goes into production and stays there — enterprise platforms, reporting systems and integrations that organisations depend on every day. If you want ownership rather than a ticket queue, we should talk.</p>
  <div class="hero-btns"><a class="btn btn-p" href="#roles">See open roles <span class="arr">→</span></a><a class="btn btn-o" href="{LINKEDIN}" target="_blank" rel="noopener">Follow us on LinkedIn</a></div>
</div></header>

<section class="sec" id="roles" aria-labelledby="roles-h"><div class="ct">
  <div class="sec-hd split"><div><div class="kicker">Open roles</div><h2 class="h2" id="roles-h">Where we're <em>hiring now.</em></h2></div>
  <p class="lede">Our team is based in Coonoor, near Ooty. Full-time roles are hybrid; internships are fully remote. Select a role for the detail.</p></div>
  <div class="roles">{rhtml}</div>
  <p class="lede" style="font-size:1rem;margin-top:2rem">Nothing quite fits? Write to <a href="mailto:{EMAIL}">{EMAIL}</a> and tell us what you'd want to work on.</p>
</div></section>

<section class="sec sec-tint"><div class="ct">
  <div class="sec-hd"><div class="kicker">Why Altherix</div><h2 class="h2">What working here <em>actually looks like.</em></h2></div>
  <div class="hire-steps">{''.join(f'<div class="rv"><span>0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(why))}</div>
</div></section>

<section class="sec"><div class="ct">
  <div class="sec-hd split"><div><div class="kicker">How we hire</div><h2 class="h2">Four steps. <em>No trick questions.</em></h2></div><p class="lede">The process usually takes two to three weeks, and you'll hear from us at every stage.</p></div>
  <div class="hire-steps">{''.join(f'<div class="rv"><span>STEP 0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps))}</div>
</div></section>

<section class="sec sec-tint"><div class="ct">
  <div class="sec-hd"><div class="kicker">The package</div><h2 class="h2">What we offer <em>beyond the pay.</em></h2></div>
  <div class="benefits">{''.join(f'<div class="rv{" hl" if hl else ""}"><h3>{t}</h3><p>{d}</p></div>' for t, d, hl in bene)}</div>
</div></section>

<section class="sec"><div class="ct"><div class="band rv">
  <div><h2>Think you'd fit in here?</h2><p>Send your CV and a short note about the work you want to be doing. Three honest paragraphs beat a keyword-stuffed profile.</p></div>
  <div class="btns"><a class="btn btn-p" href="{apply('General application', std_body.format(r='a suitable'))}">{EMAIL} <span class="arr">→</span></a><a class="btn btn-o" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></div>
</div></div></section>
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.7"))

def notfound():
    html = head("Page not found | Altherix", "This page doesn't exist.", "404.html") .replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"') + nav() + f"""
<main id="main"><section class="nf page-hero" style="border:0"><div class="ct">
  <div class="kicker">404</div><h1>This page isn't <em class="grad-text" style="font-style:normal">in production.</em></h1>
  <p class="lede">The link may be old or mistyped.</p>
  <div class="hero-btns"><a class="btn btn-p" href="/">Go to the homepage <span class="arr">→</span></a><a class="btn btn-o" href="/case-studies/">View case studies</a></div>
</div></section></main>
""" + footer()
    write("404.html", html)

def seo_files():
    import datetime
    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{url_for(p)}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

if __name__ == "__main__":
    home(); cases_index()
    for c in CASES: case_page(c)
    for s in SERVICES: service_page(s)
    careers(); notfound(); seo_files()
    print(f"Built {len(PAGES)} pages + 404, sitemap.xml, robots.txt")
