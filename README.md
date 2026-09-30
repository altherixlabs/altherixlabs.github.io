# altherix.in

Static website for Altherix Solutions, served by GitHub Pages (custom domain in `CNAME`).

## Editing

Pages are generated — don't hand-edit the HTML.

1. Change content in `_build/content.py` (case studies, services, industries, team) or templates in `_build/build.py`.
2. Run `python3 _build/build.py` from the repo root.
3. Commit the regenerated HTML along with your changes.

Styles live in `assets/site.css`, behaviour in `assets/site.js` (no frameworks, no third-party scripts). Fonts (Inter, JetBrains Mono) are self-hosted in `assets/fonts/`.

Only publish real work and real figures — no invented clients, metrics or certifications.

## Structure

- `/` — home
- `/case-studies/` and `/case-studies/<slug>/`
- `/services/<slug>/` — software-engineering, modernization, ai-automation, enterprise-integration
- `/careers.html`
- `sitemap.xml`, `robots.txt`, `404.html`

Contact: contact@altherix.in · +91 81529 23515 · https://www.linkedin.com/company/altherix
