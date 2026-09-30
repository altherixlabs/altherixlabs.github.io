#!/usr/bin/env python3
"""Static site generator for altherix.in.
Run from the repo root:  python3 _build/build.py
Writes plain HTML files; GitHub Pages serves them as-is (Jekyll ignores _build/)."""
import json, os, sys, datetime
from html import escape as E
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = []
V = "4"  # asset cache-buster

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

def url_for(path):
    return SITE + "/" + path.replace("index.html", "")

def dot(items):
    # keep each separator attached to the item before it, so wrapped lines never start with "·"
    return "\u00a0· ".join(E(t).replace(" ", "\u00a0") if len(t) < 18 else E(t) for t in items)

# ── chrome ───────────────────────────────────────────────────────────────────
NAV = [("Services", "/#services", "services"), ("Solutions", "/#solutions", "solutions"),
       ("Case Studies", "/case-studies/", "case-studies"), ("Industries", "/#industries", "industries"),
       ("About", "/#about", "about"), ("Careers", "/careers.html", "careers")]

def head(title, desc, path, jsonld=None, og_type="website", noindex=False):
    u = url_for(path)
    ld = "".join(f'\n<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en-IN" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">{robots}
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
    ind = "".join(f'<li><a href="/#industries">{n}</a></li>' for n in ["Manufacturing", "Financial Services", "Healthcare", "Education", "Logistics", "Enterprise"])
    return f"""<footer class="foot">
  <div class="ct">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="brand" href="/"><img src="/assets/mark-96.webp" width="28" height="28" alt="" loading="lazy">ALTHERIX</a>
        <p class="foot-tag">Modern Software.<br>Intelligent Systems.<br>Real Business Value.</p>
        <p class="foot-sub meta">Transforming Software, Amplifying Value.</p>
      </div>
      <div><h2 class="label">Services</h2><ul>{svc}</ul></div>
      <div><h2 class="label">Industries</h2><ul>{ind}</ul></div>
      <div><h2 class="label">Company</h2><ul><li><a href="/#about">About</a></li><li><a href="/case-studies/">Case Studies</a></li><li><a href="/#team">Team</a></li><li><a href="/careers.html">Careers</a></li><li><a href="/#contact">Contact</a></li></ul></div>
      <div><h2 class="label">Contact</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li><li><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a></li></ul></div>
    </div>
    <div class="foot-bot meta">
      <span>© <span data-year>2026</span> Altherix Solutions</span>
      <span>Ooty · India</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

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
        out.append(f'<text class="viz-label" x="0" y="{y+3.5}">{E(name)}</text>')
        out.append(f'<line class="viz-tier" x1="118" y1="{y}" x2="{W}" y2="{y}"/>')
    paths = []
    for a in range(len(tiers) - 1):
        _, y1, xs1 = tiers[a]; _, y2, xs2 = tiers[a + 1]
        for i, x1 in enumerate(xs1):
            for j, x2 in enumerate(xs2):
                if abs(i / max(1, len(xs1) - 1) - j / max(1, len(xs2) - 1)) <= 0.4:
                    my = (y1 + y2) / 2
                    paths.append(f"M{x1} {y1+6} C{x1} {my} {x2} {my} {x2} {y2-6}")
    out += [f'<path class="viz-line" d="{p}"/>' for p in paths]
    out += [f'<path class="viz-flow" d="{p}" style="animation-delay:-{(k*1.3)%9:.1f}s"/>' for k, p in enumerate(paths) if k % 3 == 0]
    for ti, (name, y, xs) in enumerate(tiers):
        for i, x in enumerate(xs):
            if ti == 2 and i == 2:
                out.append(f'<circle class="viz-core" cx="{x}" cy="{y}" r="6"/>')
            else:
                out.append(f'<circle class="viz-node" cx="{x}" cy="{y}" r="5"/>')
    out.append("</svg>")
    return "\n".join(out)

# ── components ───────────────────────────────────────────────────────────────
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
    return f"""<section class="sec" id="contact" aria-labelledby="contact-h">
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
      <p class="meta">This opens your email app with the message addressed to {EMAIL}.</p>
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
    outcomes = [("85%", "Less manual work", "ERP inventory module", "erp-inventory-module"),
                ("90%", "Time saved", "Accounting integration", "accounting-software-integration"),
                ("70%", "Fewer no-shows", "Clinic management, 4 clinics", "clinic-management-enhancement"),
                ("35%", "Higher conversions", "Payment integration", "payment-gateway-integration"),
                ("40%", "Faster deliveries", "Delivery management", "delivery-management-system"),
                ("8K+", "Active students", "Learning platform", "learning-platform-features")]
    out_html = "".join(f'<a class="outcome" href="/case-studies/{s}/"><span class="n">{n}</span><span class="l">{l}</span><span class="s">{d}</span></a>' for n, l, d, s in outcomes)

    svc_rows = ""
    for s in SERVICES:
        svc_rows += f"""<div class="row svc-row rv">
  <span class="idx">{s['n']}</span>
  <div><h3 class="h3-lg">{s['name']}</h3><p class="body">{E(s['short'])}</p><p class="stack-line">{dot(s['tech'][:6])}</p></div>
  <ul>{''.join(f'<li>{E(x)}</li>' for x in s['list'])}</ul>
  <a class="more" href="/services/{s['slug']}/" aria-label="{s['name']}: learn more">Learn more <span class="arr" aria-hidden="true">→</span></a>
</div>"""
    svc_rows += """<div class="row svc-row rv">
  <span class="idx">05</span>
  <div><h3 class="h3-lg">Cloud &amp; DevOps</h3><p class="body">Part of every engagement, and available on its own: pipelines, hardened infrastructure and monitoring that catches problems before your users do.</p><p class="stack-line">Azure · Azure DevOps · GitHub Actions · AWS S3</p></div>
  <ul><li>CI/CD pipelines</li><li>Cloud infrastructure</li><li>Monitoring &amp; alerting</li><li>Cloud migration</li></ul>
  <a class="more" href="/services/enterprise-integration/#cloud" aria-label="Cloud and DevOps: learn more">Learn more <span class="arr" aria-hidden="true">→</span></a>
</div>"""

    panels = "\n".join(cs_panel(CASE[s]) for s in ["church-management-system", "missions-office-enterprise-system", "erp-inventory-module"])

    ai_areas = [("AI Integration", "Connect AI capabilities to existing business applications."),
                ("AI Agents", "Automate multi-step workflows with appropriate human oversight."),
                ("Intelligent Automation", "Turn repetitive operational processes into adaptive workflows."),
                ("Enterprise AI", "Build secure, governed AI experiences around business data.")]
    ai_html = "".join(f'<div><h3 class="h3">{t}</h3><p class="body">{d}</p></div>' for t, d in ai_areas)

    layers = [("Experience", "Web, mobile and dashboards", ["React", "TypeScript", "Angular", "React Native", "Chart.js"]),
              ("Applications", "Domain logic and workflows", [".NET 9", "Spring Boot", "Laravel", "Django", "Node.js"]),
              ("APIs, services & AI", "Contracts between systems", ["REST", "SignalR", "Hangfire", "LLM integration", "Payment and messaging APIs"]),
              ("Data & enterprise systems", "Records, reporting and ERP", ["SQL Server", "MySQL", "PostgreSQL", "MongoDB", "SAP", "Tally", "Zoho Books"]),
              ("Cloud & DevOps", "Run, release and observe", ["Azure App Service", "Azure SQL", "Blob Storage", "AWS S3", "Azure DevOps", "GitHub Actions"])]
    layer_html = "".join(f'<li class="layer"><div><h3 class="h3">{n}</h3><p class="meta">{sub}</p></div><p class="stack-line">{dot(t)}</p></li>' for n, sub, t in layers)

    inds = "".join(f'<div class="ind rv"><h3 class="h3">{n}</h3><p class="body">{d}</p><a class="more" href="/case-studies/{slugs[0]}/">{E(CASE[slugs[0]]["title"])} <span class="arr" aria-hidden="true">→</span></a></div>' for n, d, slugs in INDUSTRIES)

    principles = [("We improve before we replace.", "Existing systems often contain years of business knowledge. We modernize intelligently instead of rewriting everything unnecessarily."),
                  ("Engineers stay close to the problem.", "Architecture, development and delivery remain connected. The people who scope your system build it and support it."),
                  ("Production is the finish line.", "We care about deployment, reliability, observability and real-world operation — not just prototypes."),
                  ("Technology follows the problem.", "We choose the architecture and stack for the problem in front of us, rather than forcing every project into the same solution.")]
    pr_html = "".join(f'<div class="row pr-row rv"><span class="idx">0{i+1}</span><h3 class="h3-lg">{t}</h3><p class="body">{d}</p></div>' for i, (t, d) in enumerate(principles))

    practices = [("Security", ["Role-based access across production platforms", "Hierarchy-scoped queries: users retrieve only their own data", "Secrets kept out of code"]),
                 ("Reliability", ["Logging, monitoring and alerting", "Backups kept in good order", "Scheduled work handled by background jobs"]),
                 ("Delivery", ["CI/CD on Azure DevOps and GitHub Actions", "Gated releases to production", "Code review, with tests written alongside code"]),
                 ("Governance", ["Audit trails on enterprise platforms", "Exports stamped with scope, period and origin", "Access enforced at the data layer, not only the UI"])]
    prac_html = "".join(f'<div class="rv"><h3 class="h3">{t}</h3><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>' for t, items in practices)

    team = "".join(f'<div class="row team-row"><h3 class="h3">{n}</h3><p class="body">{r}</p><p class="meta">{dot(ex)}</p></div>' for n, r, ini, ex in TEAM)

    jsonld = [ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "Altherix", "url": SITE + "/"}]
    html = head("Altherix | Software Engineering, AI & Enterprise Modernization",
                "Altherix engineers modern software, enterprise integrations and production-ready AI systems for businesses that depend on their technology.",
                path, jsonld) + nav() + f"""
<main id="main">

<section class="hero" aria-labelledby="hero-h">
  <div class="ct">
    <div>
      <span class="label">Software engineering company · Ooty, India</span>
      <h1 class="h1" id="hero-h"><span>Modern Software.</span><span>Intelligent Systems.</span><span class="sig">Real Business Value.</span></h1>
      <p class="lede">Altherix engineers, modernizes and intelligently automates the software systems businesses depend on.</p>
      <p class="hero-caps">Software Engineering · Modernization · AI &amp; Automation · Enterprise Integration</p>
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
    <h2 class="label" id="proof-h" style="margin-bottom:1.25rem">Outcomes from delivered work</h2>
    <div class="outcomes rv">{out_html}</div>
    <p class="proof-note meta">Figures reported on client engagements. Select one to read the case study.</p>
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
    {sec_head("Selected work", "What we built, <span class='mute'>and what it changed.</span>", "Two production platforms for a global organisation, and a module that removed most of a manufacturer's manual inventory work.", "work-h")}
    <div class="cs-list">{panels}</div>
    <div class="after"><a class="btn btn-s" href="/case-studies/">All {len(CASES)} case studies</a></div>
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
    <div class="grid2 rv" style="align-self:start">{ai_html}</div>
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

<section class="sec" id="industries" aria-labelledby="ind-h">
  <div class="ct">
    {sec_head("Industries", "Engineering across complex domains.", "Each of these comes from delivered work.", "ind-h")}
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

<section class="sec" id="team" aria-labelledby="team-h">
  <div class="ct">
    <div class="sec-hd split rv"><div><span class="label">Team</span><h2 class="h2" id="team-h" style="margin-top:1.25rem">People behind the systems.</h2></div><p class="team-note">Built by engineers who have spent years solving real software problems.</p></div>
    <div class="rows rv">{team}</div>
  </div>
</section>

<section class="sec" id="about" aria-labelledby="about-h">
  <div class="ct two even">
    <div class="prose rv">
      <span class="label">About</span>
      <h2 class="h2" id="about-h" style="margin-top:1.25rem">Global engineering. <span class="mute">Rooted in the Nilgiris.</span></h2>
      <p>Altherix was founded in Ooty, high in the Nilgiris. It's an unusual place for an engineering company, and a deliberate one: a small, senior team with room to do careful work, away from the churn of a large delivery centre.</p>
      <p>The work reaches well beyond the hills. Platforms we built run in production on Azure in the UK for a global organisation, alongside systems for manufacturers, clinics, education, logistics and finance teams in India.</p>
      <p>One conviction hasn't changed: your existing software is the backbone of your business, and it usually deserves improving before it deserves replacing.</p>
    </div>
    <dl class="facts-dl rv" style="align-self:end">
      <div><dt>Founded</dt><dd>Ooty, the Nilgiris</dd></div>
      <div><dt>Office</dt><dd>Coonoor, Tamil Nadu</dd></div>
      <div><dt>In production</dt><dd>Azure UK South · India</dd></div>
      <div><dt>Sectors</dt><dd>Nonprofit, manufacturing, finance, healthcare, education, logistics</dd></div>
      <div><dt>Company</dt><dd>Altherix Solutions</dd></div>
    </dl>
  </div>
</section>

{contact_section()}

</main>
""" + footer()
    write(path, html); PAGES.append((path, "1.0"))

# ── CASE STUDIES INDEX ───────────────────────────────────────────────────────
def cases_index():
    path = "case-studies/index.html"
    feat = [c for c in CASES if c.get("featured")]
    rest = [c for c in CASES if not c.get("featured")]
    html = head("Case Studies | Altherix", "Production systems Altherix has designed, built and integrated, with the problem, the engineering and the measurable outcome for each.", path,
                [ORG, crumbs_ld([("Home", "/"), ("Case Studies", "/case-studies/")])]) + nav("case-studies") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  {crumbs([("Home", "/"), ("Case Studies", "/case-studies/")])}
  <span class="label">Case studies</span>
  <h1 class="h1">Production systems and what they changed.</h1>
  <p class="lede">{len(CASES)} engagements across nonprofit, manufacturing, finance, healthcare, education and logistics.</p>
</div></header>
<section class="sec"><div class="ct">
  <h2 class="label" style="margin-bottom:1.25rem">Featured engagement · The Church of Pentecost</h2>
  <div class="cs-list">{''.join(cs_panel(c) for c in feat)}</div>
</div></section>
<section class="sec"><div class="ct">
  {sec_head("More work", "Focused systems, <span class='mute'>measurable results.</span>", None, "more-h")}
  <div class="rows">{''.join(cs_row(c) for c in rest)}</div>
</div></section>
{contact_section("Discuss a similar problem.", "Tell us about the system you're working with and what a good outcome looks like. An engineer will reply.")}
</main>
""" + footer()
    write(path, html); PAGES.append((path, "0.9"))

# ── CASE STUDY PAGE ──────────────────────────────────────────────────────────
def case_page(c):
    path = f"case-studies/{c['slug']}/index.html"
    svc = SERVICE[c["related_service"]]
    toc = [("summary", "Summary"), ("challenge", "The challenge"), ("approach", "The approach"), ("architecture", "Architecture"),
           ("engineering", "Engineering"), ("technology", "Technology"), ("results", "Results"), ("impact", "Impact")]
    related = [x for x in CASES if x["slug"] != c["slug"] and (x["industry"] == c["industry"] or x["related_service"] == c["related_service"])][:3]
    facts = [("Category", c["category"]), ("Industry", c["industry"])]
    if c.get("client"): facts.insert(0, ("Client", c["client"]))
    if c.get("featured"): facts.append(("Status", "Live in production"))
    jsonld = [ORG, crumbs_ld([("Home", "/"), ("Case Studies", "/case-studies/"), (c["title"], f"/case-studies/{c['slug']}/")]),
              {"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "description": c["oneliner"],
               "author": {"@type": "Organization", "name": "Altherix Solutions"},
               "publisher": {"@type": "Organization", "name": "Altherix Solutions", "logo": {"@type": "ImageObject", "url": SITE + "/assets/icon-512.png"}},
               "image": SITE + "/assets/og.png", "mainEntityOfPage": url_for(path)}]
    rel = f'<section class="sec"><div class="ct">{sec_head("More work", "Related case studies", None, "rel-h")}<div class="rows">{"".join(cs_row(r) for r in related)}</div></div></section>' if related else ""
    html = head(f"{c['title']}: Case Study | Altherix", c["oneliner"], path, jsonld, "article") + nav("case-studies") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  {crumbs([("Home", "/"), ("Case Studies", "/case-studies/"), (c['title'], "")])}
  <span class="label">{E(c['category'])}</span>
  <h1 class="h1">{E(c['title'])}</h1>
  <p class="lede">{E(c['oneliner'])}</p>
  <dl class="facts">{''.join(f'<div><dt>{k}</dt><dd>{E(v)}</dd></div>' for k, v in facts)}</dl>
</div></header>
<section class="sec"><div class="ct article">
  <nav class="toc" aria-label="On this page">{''.join(f'<a href="#{i}">{t}</a>' for i, t in toc)}</nav>
  <div>
    <div class="block" id="summary"><h2 class="h3-lg">Summary</h2><p>{E(c['summary'])}</p></div>
    <div class="block" id="challenge"><h2 class="h3-lg">The challenge</h2>{''.join(f'<p>{E(p)}</p>' for p in c['challenge'])}</div>
    <div class="block" id="approach"><h2 class="h3-lg">The approach</h2><ul class="plist">{''.join(f'<li><b>{E(a)}.</b> {E(b)}</li>' for a, b in c['approach'])}</ul></div>
    <div class="block" id="architecture"><h2 class="h3-lg">Architecture</h2><dl class="kv">{''.join(f'<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in c['architecture'])}</dl></div>
    <div class="block" id="engineering"><h2 class="h3-lg">Engineering</h2><dl class="kv">{''.join(f'<div><dt>{E(a)}</dt><dd>{E(b[0].upper() + b[1:])}.</dd></div>' for a, b in c['engineering'])}</dl></div>
    <div class="block" id="technology"><h2 class="h3-lg">Technology</h2><p class="stack-line" style="font-size:.875rem">{dot(c['tech'])}</p></div>
    <div class="block" id="results"><h2 class="h3-lg">Results</h2><span class="label">Key metrics</span><div class="metrics" style="margin-top:.75rem">{''.join(f'<div><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in c['metrics'])}</div></div>
    <div class="block" id="impact"><h2 class="h3-lg">Impact</h2><p>{E(c['impact'])}</p><p style="margin-top:1.5rem"><a class="more" href="/services/{svc['slug']}/">Related service: {svc['name']} <span class="arr" aria-hidden="true">→</span></a></p></div>
  </div>
</div></section>
{rel}
{contact_section("Discuss a similar problem.", "If this looks like something you're dealing with, tell us about your system. An engineer will reply.")}
</main>
""" + footer()
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
              {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": s["short"], "provider": {"@type": "Organization", "name": "Altherix Solutions", "url": SITE + "/"}, "areaServed": "Worldwide"}]
    h1 = s["h1"].replace("<em>", '<span class="mute">').replace("</em>", "</span>")
    html = head(f"{s['name']} | Altherix", s["short"], path, jsonld) + nav("services") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  {crumbs([("Home", "/"), ("Services", "/#services"), (s['name'], "")])}
  <span class="label">{s['name']}</span>
  <h1 class="h1">{h1}</h1>
  <p class="lede">{E(s['lede'])}</p>
  <div class="btns"><a class="btn btn-p" href="#contact">Talk to an Engineer</a><a class="btn btn-s" href="#work">Relevant work</a></div>
</div></header>
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
    html = head("Careers | Altherix", "Join Altherix, a senior engineering team in the Nilgiris building production systems. Open roles include a fully remote Full Stack Development internship.", path,
                [ORG, crumbs_ld([("Home", "/"), ("Careers", "/careers.html")])] + jobs) + nav("careers") + f"""
<main id="main">
<header class="page-hero"><div class="ct">
  {crumbs([("Home", "/"), ("Careers", "")])}
  <span class="label">Careers</span>
  <h1 class="h1">Small team. <span class="mute">Serious systems.</span></h1>
  <p class="lede">Our work goes into production and stays there: enterprise platforms, reporting systems and integrations that organisations depend on every day. If you want ownership rather than a ticket queue, we should talk.</p>
  <div class="btns"><a class="btn btn-p" href="#roles">See open roles</a><a class="more" href="{LINKEDIN}" target="_blank" rel="noopener">Follow Altherix on LinkedIn <span class="arr" aria-hidden="true">→</span></a></div>
</div></header>

<section class="sec" id="roles" aria-labelledby="roles-h"><div class="ct">
  {sec_head("Open roles", "Where we're hiring.", "Our team is based in Coonoor, near Ooty. Full-time roles are hybrid; internships are fully remote.", "roles-h")}
  <div class="roles">{rhtml}</div>
  <p class="body" style="margin-top:2rem">Nothing quite fits? Write to <a href="mailto:{EMAIL}">{EMAIL}</a> and tell us what you'd want to work on.</p>
</div></section>

<section class="sec"><div class="ct">
  {sec_head("Working here", "What the work is actually like.", None, "why-h")}
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

def notfound():
    html = head("Page not found | Altherix", "This page doesn't exist.", "404.html", noindex=True) + nav() + """
<main id="main"><section class="nf page-hero"><div class="ct">
  <span class="label">404</span><h1 class="h1">This page isn't in production.</h1>
  <p class="lede">The link may be old or mistyped.</p>
  <div class="btns"><a class="btn btn-p" href="/">Go to the homepage</a><a class="btn btn-s" href="/case-studies/">View case studies</a></div>
</div></section></main>
""" + footer()
    write("404.html", html)

def seo_files():
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
