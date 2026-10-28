"""Site content. Everything here comes from material already published on altherix.in
(case studies, services, products, careers). Do not add clients, figures or certifications
that are not supported by real work."""

SITE = "https://altherix.in"
EMAIL = "contact@altherix.in"
PHONE_DISPLAY = "+91 81529 23515"
PHONE_TEL = "+918152923515"
LINKEDIN = "https://www.linkedin.com/company/altherix"
ADDRESS = ["1247 N1, LN Gardens, Stanley Park", "Ottupattarai, Coonoor", "Nilgiris, Tamil Nadu 643105"]

# Search Console / Bing Webmaster verification codes. Paste the content value only; leave empty to omit the tag.
GOOGLE_SITE_VERIFICATION = ""
BING_SITE_VERIFICATION = "3094D6A701575725433D5DD1A488F48D"

# Page titles and meta descriptions for pages that aren't a case study or service.
# Titles 50–60 characters, descriptions 140–160. Visible headings are set in build.py.
SEO = {
  "home": dict(seo_title="Software Development & Modernization in India | Altherix",
               seo_desc="Software engineering company in India for clients in India, the UK and Europe: custom software, modernization, AI automation and integration.",
               kw_sub="Software development, modernization and AI automation for businesses in India, the UK and Europe."),
  "case-studies": dict(seo_title="Software Development & Integration Case Studies | Altherix",
                       seo_desc="Production platforms built and run by Altherix for The Church of Pentecost: a .NET 9 church management system and a Laravel reporting system on Azure."),
  "products": dict(seo_title="Products: CodeGate & Mandate | Altherix",
                   seo_desc="CodeGate ranks developer candidates with hidden tests and AI grading. Mandate is a safe gateway between AI agents and your ERP, SQL and in-house systems."),
  "careers": dict(seo_title="Remote Full Stack Internship, ₹10,000 Stipend | Altherix",
                  seo_desc="Now hiring: remote Full Stack Development interns, 2 or 3 months, ₹10,000 a month stipend and a paid 3-day onsite in Ooty. Plus full-time engineering roles."),
}

# Home page FAQ — shown on the page and as FAQPage structured data. Keep answers factual.
FAQ = [
  ("What does Altherix do?",
   "Altherix is a small software engineering company. We build custom web applications and enterprise platforms, modernize existing systems, add automation and AI where it helps, and connect business systems to each other. We also deploy and run what we build."),
  ("Why choose a focused team over a large agency?",
   "You work directly with the engineers who design, build and run your system, with no account managers or hand-offs. Our platforms run in production on Azure for clients in the UK and Ghana, including a church management system with 80+ API modules and statistical reporting across seven organisational levels, and we'll walk you through how they're built."),
  ("Which technologies do you work with?",
   "Our production work is in .NET 9 and ASP.NET Core, React and TypeScript, Laravel and PHP, SQL Server and MySQL, on Azure with Azure DevOps pipelines. We choose the stack that suits your system rather than forcing one."),
  ("How does an engagement start?",
   "With a free 30-minute call with an engineer. We then review your existing system and send a written assessment with options, followed by a proposal: fixed scope and price for defined work, or a monthly team for ongoing work. Build work happens in two-week increments you can see and use."),
  ("How much does it cost, and how quickly can you deliver?",
   "Our rates are well below those of UK, European and US agencies, and defined work gets a fixed price agreed before we start. You'll have working software within two weeks of starting, followed by a new increment every two weeks."),
  ("Can we start with something small?",
   "Yes, and we recommend it. Start with a written assessment or a single module. If it works for you, we carry on; if not, you haven't committed to a large project."),
  ("Do you offer a referral discount?",
   "Yes. If you refer a client to us, both you and the client you refer get a 5 to 10% discount."),
  ("Where is Altherix based?",
   "Our office is in Coonoor, in the Nilgiris district of Tamil Nadu, India. Altherix was founded in nearby Ooty. We take on projects remotely across India, the UK and Europe."),
]

# ────────────────────────────────────────────────────────────────────────────
# CASE STUDIES
# ────────────────────────────────────────────────────────────────────────────
CASES = [
  dict(
    slug="church-management-system",
    shots=[("cms-overview", "Church Management System overview screen: transfer approvals, totals for members, groups and events, and a membership summary by age group and gender.", "Overview: approvals, totals and membership summary (member names blurred)"),
           ("cms-leaders", "Church Management System leaders dashboard: headline figures for members, souls won, officers, home cells and more, with period comparison and area performance.", "Leaders dashboard: headline figures against the previous period")],
    seo_desc=".NET 9, React and SQL Server church management platform on Azure, with live check-in over SignalR and Hangfire jobs: 80+ API modules in production.",
    featured=True,
    category="Non-profit · Enterprise platform",
    industry="Enterprise / Nonprofit",
    title="Church Management System",
    client="The Church of Pentecost",
    oneliner="A congregation management platform replacing spreadsheets and paper registers with one record of every member, group, event and attendance.",
    summary="For The Church of Pentecost, Altherix designed, built and deployed a full congregation management platform. It replaced spreadsheets and paper registers with a single record of every member, group, event and attendance across the organisation's assemblies, and runs in production on Azure.",
    problem="Member records, groups, events and attendance lived in spreadsheets and paper registers spread across assemblies.",
    solution="One platform for the member lifecycle, recurring events, real-time check-in, inter-assembly transfers and leadership analytics.",
    challenge=[
      "Congregation data was held in spreadsheets and paper registers, so there was no single, reliable record of members, groups, events or attendance across assemblies.",
      "The platform had to handle the real shape of church life: households and home cells, members moving between assemblies, services that recur every week with exceptions, and visitors who arrive without a record.",
    ],
    approach=[
      ("Model the domain first", "Member lifecycle — education and career history, salvation and baptism status, household and home-cell membership — modelled as first-class data rather than free text."),
      ("Automate the paperwork", "Inter-assembly transfers run as a request workflow that generates the transfer letter automatically."),
      ("Treat recurrence properly", "Recurring services are expanded into individual occurrences by a scheduled background job, so each occurrence can carry its own exceptions."),
      ("Migrate, don't retype", "Excel import and export so existing registers could be brought across in bulk."),
    ],
    architecture=[
      ("Experience", "React 18 and TypeScript front end with MUI and Redux Toolkit"),
      ("Application", "ASP.NET Core on .NET 9 — membership, events, attendance, transfers and reporting modules"),
      ("Real-time & jobs", "SignalR for live check-in over WebSockets; Hangfire for scheduled recurrence expansion"),
      ("Data", "SQL Server through Entity Framework Core"),
      ("Cloud", "Azure (UK South), released through a gated pipeline"),
    ],
    engineering=[
      ("Live check-in", "real-time attendance capture over WebSockets, including visitors and anonymous attendees"),
      ("Background processing", "recurring events expanded into occurrences by a scheduled job, with per-occurrence exceptions"),
      ("Bulk data", "Excel import and export for migrating existing registers"),
      ("Reporting", "dashboards and generated PDF reports for leadership"),
      ("Controls", "role-based access and audit logging throughout"),
    ],
    tech=[".NET 9", "ASP.NET Core", "EF Core", "SQL Server", "SignalR", "Hangfire", "React 18", "TypeScript", "MUI", "Redux Toolkit", "Azure"],
    metrics=[("80+", "API modules"), ("2", "Connected apps"), ("Live", "In production on Azure")],
    headline=("80+", "API modules in production"),
    impact="Congregation operations moved from paper and spreadsheets onto one system of record, live in production and delivered as part of a multi-year engagement that also produced the Missions Office Enterprise System.",
    related_service="software-engineering",
  ),
  dict(
    slug="missions-office-enterprise-system",
    shots=[("missions-dashboard", "Missions Office statistics dashboard: reporting period selector, drill-down by administration, CSV and PDF export, and tabs for membership, evangelism, attendance, ministry and children, estates, Vision 2028 and data completeness.", "Statistics dashboard: drill-down by administration, period comparison and exports")],
    seo_desc="Laravel 12 and MySQL reporting system on Azure App Service: statistical returns across a seven-level hierarchy, six dashboard modules and audited exports.",
    featured=True,
    category="Non-profit · Enterprise reporting",
    industry="Enterprise / Nonprofit",
    title="Missions Office Enterprise System",
    client="The Church of Pentecost",
    oneliner="Global statistical reporting consolidated across a seven-tier organisational hierarchy, with drill-down dashboards and audited exports.",
    summary="A reporting and analytics system for the Church of Pentecost's global Missions Office in Ghana. It consolidates half-year and end-year statistical returns submitted from every level of a seven-tier hierarchy, from the Global Office down to a single local assembly.",
    problem="Half-year and end-year statistical returns had to be consolidated across seven organisational levels, with each administrator seeing only their own branch.",
    solution="Drill-down statistics dashboards, access scoped at query level, a Vision 2028 scorecard and exports stamped with their provenance.",
    challenge=[
      "Statistical returns arrive from every level of a seven-tier hierarchy: Global Office → Regional Missions Office → Regional Committee → Nation → Area → District → Local Assembly.",
      "Leadership needed to read the same figures from the top of the organisation down to one assembly, while every administrator must only ever see the branch they are responsible for.",
    ],
    approach=[
      ("Scope at the query, not the screen", "Access is enforced at query level, so an administrator can only ever retrieve their own branch of the hierarchy."),
      ("One model, many altitudes", "Membership, evangelism, attendance, ministry and estates dashboards, each with drill-down from global to a single assembly."),
      ("Measure against the plan", "A configurable Vision 2028 scorecard with indicators, targets and pace-adjusted progress tracking."),
      ("Know what's missing", "Data-completeness tracking shows which assemblies have submitted for a period and lists those outstanding."),
    ],
    architecture=[
      ("Experience", "Server-rendered views with Alpine.js and Chart.js dashboards"),
      ("Application", "Laravel 12 on PHP 8.2 — returns, hierarchy, scorecard and export modules"),
      ("Access", "Hierarchy-scoped authorisation applied at query level"),
      ("Data", "MySQL"),
      ("Cloud", "Azure App Service, released through Azure DevOps pipelines"),
    ],
    engineering=[
      ("Seven-level hierarchy", "Global Office → Regional Missions Office → Regional Committee → Nation → Area → District → Local Assembly"),
      ("Statistics dashboards", "membership, evangelism, attendance, ministry and estates, each with drill-down"),
      ("Scoped access", "enforced at query level"),
      ("Vision 2028 scorecard", "configurable indicators and targets with pace-adjusted progress"),
      ("Exports & provenance", "CSV and PDF exports stamped with scope, period and generation trail"),
      ("Data completeness", "tracks which assemblies have submitted and which are outstanding"),
    ],
    tech=["Laravel 12", "PHP 8.2", "MySQL", "Alpine.js", "Chart.js", "dompdf", "Azure App Service", "Azure DevOps"],
    metrics=[("7", "Hierarchy levels"), ("6", "Dashboard modules"), ("Live", "In production on Azure")],
    headline=("7", "Organisational levels, one reporting system"),
    impact="Statistical reporting for a global organisation now runs through one governed system, with figures that can be traced from the Global Office down to a single assembly and exports that record exactly what they contain.",
    related_service="enterprise-integration",
  ),
]
CASE = {c["slug"]: c for c in CASES}

# ────────────────────────────────────────────────────────────────────────────
# SERVICES
# ────────────────────────────────────────────────────────────────────────────
SERVICES = [
  dict(
    slug="software-engineering", n="01", name="Software Engineering",
    seo_title="Custom Software & Enterprise App Development | Altherix",
    seo_desc="Custom software and enterprise application development in .NET, React and Laravel, built, deployed on Azure and supported by the same small team.",
    kw_sub="Custom software development and enterprise application development services.",
    short="Full-stack applications and enterprise platforms, designed, built and taken into production by the engineers who scoped them.",
    list=["Full-stack applications", "Enterprise platforms", "APIs & microservices", "Product engineering"],
    tech=[".NET 9", "ASP.NET Core", "React", "TypeScript", "Laravel", "SQL Server", "MySQL", "Azure"],
    h1="Software that goes into production and <em>stays there.</em>",
    lede="We design and build full-stack applications and enterprise platforms — the data model, the API, the front end and the deployment — and we stay with them after launch.",
    problem=[
      "Most software projects don't fail at the code. They fail at the edges: requirements that were never pinned down, a data model that can't carry the real domain, a front end nobody was consulted on, and a deployment treated as someone else's job.",
      "We keep those edges inside one team. The engineers who talk to you are the engineers who build it.",
    ],
    approach=[
      ("Scope with the people who build", "Ambiguous requirements are turned into a shippable scope by the engineers who will deliver it."),
      ("Model the domain properly", "Relational schemas designed around how your organisation actually works, so the data stays trustworthy as it grows."),
      ("Build across the stack", "APIs, background processing, real-time features and front ends designed as one system."),
      ("Own the release", "CI/CD, cloud hosting and production support are part of the work, not an afterthought."),
    ],
    caps=[
      ("Full-stack applications", "Web applications with a considered component architecture, from API to interface."),
      ("Enterprise platforms", "Multi-module systems with role-based access, audit trails and reporting — built for organisations that depend on them daily."),
      ("APIs & microservices", "REST APIs and service boundaries that other systems and teams can rely on."),
      ("Product engineering", "New features and modules for existing products — design, build, test and deploy."),
      ("Real-time & background work", "WebSocket features (SignalR) and scheduled jobs (Hangfire) where the problem needs them."),
    ],
    cases=["church-management-system", "missions-office-enterprise-system"],
  ),
  dict(
    slug="modernization", n="02", name="Modernization",
    seo_title="Legacy Application Modernization, Cloud Migration | Altherix",
    seo_desc="Legacy application modernization without a rewrite: .NET and PHP upgrades, architecture refactoring, cloud migration to Azure and performance engineering.",
    kw_sub="Legacy application modernization, .NET and PHP upgrades, and cloud migration services.",
    short="Improve before you replace. Upgrade stacks, refactor architecture and move to the cloud without losing the knowledge built into your systems.",
    list=["Legacy modernization", "Architecture refactoring", "Cloud migration", "Performance engineering"],
    tech=["Azure", ".NET", "Laravel", "SQL Server", "MySQL", "Azure DevOps"],
    h1="Most companies don't need <em>another rewrite.</em>",
    lede="Existing systems hold years of business rules that nobody wrote down. We modernise them deliberately — upgrading, refactoring and migrating in steps — instead of throwing them away.",
    problem=[
      "A full rewrite looks clean on a slide and is usually the riskiest option on the table. It discards knowledge encoded in the old system, stalls new features for months and often recreates the same problems on a newer stack.",
      "Modernisation should reduce risk, not move it. We start with what already works and change what doesn't.",
    ],
    approach=[
      ("Understand what's there", "Map the existing system, its data and the business rules it quietly enforces."),
      ("Change in steps", "Stack upgrades and architecture refactoring delivered incrementally, without stopping operations."),
      ("Move when it pays", "Cloud migration planned around cost, risk and what the workload actually needs."),
      ("Make it fast", "Profile first, then fix: query tuning, caching and scaling where the evidence points."),
    ],
    caps=[
      ("Technology stack upgrades", "Bring frameworks, runtimes and dependencies up to date without a rewrite."),
      ("Architecture refactoring", "Untangle modules, introduce clear service boundaries and make the codebase safe to change."),
      ("Cloud migration", "Move from on-premise or shared hosting into the cloud, primarily Azure."),
      ("Performance engineering", "Database query optimisation, caching and CDN strategy, load balancing and scaling."),
      ("Paper and spreadsheet replacement", "Turn registers and spreadsheets into a governed system of record, with bulk import of existing data."),
      ("Enhancement of live systems", "New modules added to a system that is already in use, without taking it offline."),
    ],
    cases=["church-management-system", "missions-office-enterprise-system"],
  ),
  dict(
    slug="ai-automation", n="03", name="AI & Automation",
    seo_title="AI Automation Services & AI Agents for Business | Altherix",
    seo_desc="AI automation services: AI agents for business, intelligent workflows and process automation connected to your systems, with access control, logging and review.",
    kw_sub="AI automation services, AI agents for business and process automation.",
    short="Automation that removes real manual work — and AI where it genuinely helps, built with the same engineering discipline as everything else.",
    list=["AI integrations", "AI agents", "Intelligent workflows", "Process automation"],
    tech=["Python", "LLM APIs", "Workflow orchestration", "REST integrations", "Background jobs", "Human review steps"],
    h1="AI that works <em>in production.</em>",
    lede="AI doesn't replace good engineering. It depends on it. We connect AI to the systems and data you already have, and we're just as ready to tell you when conventional automation is the better answer.",
    problem=[
      "AI doesn't fix broken processes. Most failed AI projects are integration and data problems in disguise: the model works in a demo, but it can't reach the right data, can't be trusted without review, and nobody owns it once it's live.",
      "We treat AI as one component in a production system — with access controls, logging, human oversight and a clear definition of what \"working\" means.",
    ],
    approach=[
      ("Start with the process", "Find where the manual effort actually is. Often the right answer is conventional automation."),
      ("Connect to real data", "AI is only as useful as the business data and systems it can safely reach."),
      ("Keep a human in the loop", "Multi-step automation with review points where the stakes justify them."),
      ("Run it like software", "Deployed, logged, access-controlled and monitored like everything else we ship."),
    ],
    caps=[
      ("AI integration", "Connect AI capabilities to existing business applications."),
      ("AI agents", "Automate multi-step workflows with appropriate human oversight."),
      ("Intelligent automation", "Turn repetitive operational processes into adaptive workflows."),
      ("Enterprise AI", "Build secure, governed AI experiences around business data."),
      ("Process automation", "Invoicing, reconciliation, reminders, alerts and scheduled jobs that remove repetitive work."),
      ("Automation you can audit", "Logging, audit trails and scoped access built in from the start."),
    ],
    cases=["church-management-system", "missions-office-enterprise-system"],
    cases_title="Automation already in production",
    cases_note="Scheduled background jobs, live check-in and data-completeness tracking in our client platforms, plus CodeGate, our own product, which combines hidden tests with AI grading.",
  ),
  dict(
    slug="enterprise-integration", n="04", name="Enterprise Integration",
    seo_title="ERP, SAP, Tally & Payment Gateway Integration | Altherix",
    seo_desc="ERP and SAP integration, Tally and Zoho Books integration, and payment gateway integration with Razorpay, PayU and Paytm, plus CI/CD and Azure cloud operations.",
    kw_sub="ERP and SAP integration, Tally and Zoho Books integration, and payment gateway integration services.",
    short="Connect business systems so data moves once, correctly — SAP and ERP, accounting, payments and third-party APIs.",
    list=["SAP and enterprise integrations", "Business systems", "Data integration", "Third-party APIs"],
    tech=["REST", "OData", "Webhooks", "SAP", "Tally", "Zoho Books", "Razorpay", "Azure DevOps"],
    h1="Systems that talk to each other, <em>correctly.</em>",
    lede="Most organisations run on several systems that were never designed to work together. We build the integrations that let data move once, accurately, without someone re-keying it.",
    problem=[
      "When systems don't connect, people become the integration layer — exporting, re-keying and reconciling by hand. It's slow, it's error-prone, and it hides the real state of the business.",
      "We build integrations as production software: versioned APIs, reconciliation, error handling and a clear record of what moved and when.",
    ],
    approach=[
      ("Map the data flow", "Understand where each piece of data originates, who owns it and where it needs to be."),
      ("Build a bridge, not a tangle", "Clean API layers between systems instead of point-to-point scripts."),
      ("Reconcile automatically", "Every integration that moves money or records gets a way to prove it balanced."),
      ("Run it in the cloud", "Pipelines, environments, monitoring and alerting so failures are seen before users see them."),
    ],
    caps=[
      ("SAP and ERP integration", "Connect enterprise and ERP systems to the applications around them."),
      ("Accounting & finance", "Billing-to-accounting bridges with automated invoicing, GST preparation and reconciliation."),
      ("Payments", "Multi-gateway integrations with UPI, wallets, EMI and reconciliation reporting."),
      ("Third-party APIs", "Messaging, mapping, video and other services integrated reliably."),
      ("Data integration & reporting", "Consolidating data across organisational levels into governed dashboards and exports."),
      ("RESTful & GraphQL APIs", "API design for systems that other teams and partners depend on."),
    ],
    cloud=dict(
      title="Cloud & DevOps",
      text="Integration only works if it keeps working. We build and maintain CI/CD pipelines across Azure DevOps and GitHub Actions, provision and harden cloud infrastructure — primarily on Azure — and set up the monitoring, logging and alerting that tells us something is wrong before you do.",
      list=["CI/CD with Azure DevOps and GitHub Actions", "Azure App Service, SQL and Blob Storage", "Gated release pipelines", "Monitoring, logging and alerting", "Secrets, backups and access control", "Containers and infrastructure-as-code"],
    ),
    cases=["missions-office-enterprise-system", "church-management-system"],
  ),
]
SERVICE = {s["slug"]: s for s in SERVICES}

# ────────────────────────────────────────────────────────────────────────────
# WHAT WE CAN BUILD. Capabilities, not track record: only "membership" is past work.
# ────────────────────────────────────────────────────────────────────────────
BUILDS = [
  ("Membership & multi-level reporting", "global", "Member records, events, live check-in and statistics across a seven-level hierarchy, in production today.", "/case-studies/missions-office-enterprise-system/", "See the work"),
  ("Inventory & operations", "manufacturing", "Stock records, barcode capture, reorder rules and the reports your operations and finance teams need.", None, None),
  ("Billing, accounting & payments", "finance", "Invoices posted to Tally or Zoho Books, payment gateways, and reconciliation that runs on a schedule.", None, None),
  ("Bookings & scheduling", "healthcare", "Appointments, reminders and records for clinics, studios and service businesses.", None, None),
  ("Learning & assessment", "education", "Courses, quizzes and certificates, and coding assessments: we built CodeGate for our own hiring.", "/products/#codegate", "See CodeGate"),
  ("Field work & delivery", "logistics", "Job dispatch, live status and customer notifications for teams on the move.", None, None),
]


# ────────────────────────────────────────────────────────────────────────────
# PRIVACY POLICY. From Altherix's Data Privacy & Protection Policy (v5.0, effective May 2023).
# Web changes: privacy contact is contact@altherix.in (the only published address),
# no personal signature, list numbering corrected, and a short "This website" section added.
# Each section: (heading, [blocks]); a block is a paragraph string or a list of bullet strings.
# ────────────────────────────────────────────────────────────────────────────
PRIVACY_META = dict(version="5.0", effective="May 2023")
PRIVACY = [
  ("This website", [
    "altherix.in sets no cookies and loads no analytics, advertising or tracking scripts. Our fonts and images are served from this site.",
    "The contact form does not send anything to our servers. It opens your own email app with your message addressed to contact@altherix.in, and you decide whether to send it. If you do, we use your message and contact details only to reply and to discuss the work you asked about.",
  ]),
  ("1. Introduction", [
    "Altherix is committed to protecting the privacy and security of personal data and sensitive information entrusted to us by our clients, partners, and service users. This Data Privacy & Protection Policy outlines our principles, practices, and obligations regarding the collection, processing, storage, and protection of personal and confidential data in accordance with applicable data protection regulations including the General Data Protection Regulation (GDPR), the Indian Information Technology Act, 2000, and other relevant data privacy laws.",
  ]),
  ("2. Definitions", [[
    "<b>Personal Data:</b> Any information relating to an identified or identifiable natural person (data subject), directly or indirectly.",
    "<b>Processing:</b> Any operation performed on personal data such as collection, recording, organization, structuring, storage, adaptation, retrieval, use, disclosure, or erasure.",
    "<b>Data Controller:</b> The entity that determines the purposes and means of processing personal data (e.g., Altherix's client).",
    "<b>Data Processor:</b> The entity that processes personal data on behalf of the controller (e.g., Altherix when acting as a service provider).",
    "<b>Data Subject:</b> The individual to whom personal data relates.",
    "<b>Breach:</b> Any unauthorized or accidental access, disclosure, loss, alteration, or destruction of personal data.",
  ]]),
  ("3. Scope", [
    "This policy applies to all personal data processed by Altherix in connection with the provision of software development services, system implementation, maintenance, and support. It covers data in any format (electronic, paper, or other) and includes information about employees, contractors, clients, end users, and third parties.",
  ]),
  ("4. Data Processing Principles", [
    "Altherix adheres to the following core principles in all data processing activities:",
    [
      "<b>Lawfulness, Fairness &amp; Transparency:</b> Data is processed lawfully, fairly, and transparently with respect to the data subject.",
      "<b>Purpose Limitation:</b> Data is collected for specified, explicit, and legitimate purposes and not further processed in a manner incompatible with those purposes.",
      "<b>Data Minimization:</b> Only necessary and relevant personal data is collected and processed.",
      "<b>Accuracy:</b> Personal data is kept accurate and up-to-date; reasonable steps are taken to erase or correct inaccurate data.",
      "<b>Storage Limitation:</b> Personal data is kept in a form which permits identification of data subjects for no longer than necessary.",
      "<b>Integrity &amp; Confidentiality:</b> Personal data is processed securely with appropriate protection against unauthorized access, loss, or damage.",
      "<b>Accountability:</b> Altherix is responsible for demonstrating compliance with these principles.",
    ],
  ]),
  ("5. Types of Data Collected", [
    "<b>5.1 Employee &amp; Contractor Data</b>",
    ["Name, contact information, employment history", "Tax identification numbers, bank details", "Performance records, training history"],
    "<b>5.2 Client &amp; End-User Data</b>",
    ["Business contact information", "Transactional and usage data related to services provided", "Communication records (emails, logs)"],
    "<b>5.3 Third-Party &amp; Sensitive Data</b>",
    ["Any personal data of third parties included in client data or business documents", "Financial, health, or other sensitive categories processed only with explicit consent and appropriate safeguards"],
  ]),
  ("6. Legal Basis for Processing", [
    "Altherix processes personal data only when we have a lawful basis, including:",
    [
      "<b>Contractual Necessity:</b> Data processing required to fulfill contractual obligations",
      "<b>Legal Obligation:</b> Compliance with laws, regulations, and government requests",
      "<b>Legitimate Interest:</b> Processing necessary for Altherix's legitimate business operations (security, fraud prevention)",
      "<b>Consent:</b> Explicit consent from the data subject for specific purposes",
      "<b>Vital Interest:</b> Protection of life or health in emergency situations",
    ],
  ]),
  ("7. Data Security & Protection Measures", [
    "Altherix implements comprehensive technical, organizational, and administrative safeguards to protect personal data:",
    "<b>7.1 Technical Measures</b>",
    [
      "<b>Encryption:</b> Sensitive data encrypted in transit (TLS/SSL) and at rest (AES-256)",
      "<b>Access Control:</b> Role-based access controls (RBAC) limiting data access to authorized personnel",
      "<b>Firewalls &amp; Intrusion Detection:</b> Network security infrastructure to prevent unauthorized access",
      "<b>Secure Backups:</b> Regular encrypted backups with secure recovery procedures",
      "<b>Vulnerability Management:</b> Regular security assessments, penetration testing, and patch management",
    ],
    "<b>7.2 Organizational Measures</b>",
    [
      "<b>Data Protection Training:</b> All employees receive regular data privacy and security training",
      "<b>Access Restrictions:</b> Data access restricted to personnel with legitimate business needs",
      "<b>Confidentiality Agreements:</b> All employees and contractors sign confidentiality agreements",
      "<b>Incident Response Plan:</b> Procedures to detect, investigate, and remediate security breaches",
    ],
    "<b>7.3 Administrative Measures</b>",
    [
      "<b>Data Inventory:</b> Comprehensive record of personal data processing activities",
      "<b>Data Processing Agreements:</b> Formal Data Processing Agreements (DPA) with all processors and third parties",
      "<b>Privacy Impact Assessments:</b> Conducted for high-risk processing activities",
      "<b>Audits &amp; Monitoring:</b> Regular audits of data protection practices and compliance",
    ],
  ]),
  ("8. Data Sharing & Third Parties", [
    "Altherix shares personal data with third parties only:",
    [
      "With explicit consent from the data subject or data controller",
      "When legally required (law enforcement, court orders, regulatory compliance)",
      "To trusted service providers and processors under written Data Processing Agreements",
      "In connection with business transactions (M&amp;A, asset sale) with appropriate confidentiality terms",
      "To protect rights, safety, or legitimate interests of Altherix or third parties",
    ],
    "All third-party processors are assessed for data protection capabilities and bound by written agreements specifying their obligations.",
  ]),
  ("9. International Data Transfers", [
    "Where personal data is transferred outside the country of origin, Altherix ensures adequate safeguards:",
    [
      "Standard Contractual Clauses (SCCs) for transfers to countries without adequate protection",
      "Binding Corporate Rules (BCRs) for intra-group transfers",
      "Adequacy decisions recognized by relevant data protection authorities",
      "Explicit consent from data subjects where required",
    ],
  ]),
  ("10. Data Subject Rights", [
    "Data subjects have the following rights, which Altherix respects and facilitates:",
    [
      "<b>Right of Access:</b> Request and obtain confirmation of personal data processing and receive a copy",
      "<b>Right to Rectification:</b> Request correction of inaccurate or incomplete data",
      "<b>Right to Erasure:</b> Request deletion of personal data (subject to legal retention requirements)",
      "<b>Right to Restrict Processing:</b> Request limitation of processing for specific purposes",
      "<b>Right to Data Portability:</b> Request data in structured, machine-readable format",
      "<b>Right to Object:</b> Object to processing on grounds of legitimate interest or direct marketing",
      "<b>Right Not to be Subject to Automated Decision-Making:</b> Request human review of automated decisions",
    ],
    "Requests to exercise these rights should be directed to our Data Protection Officer (contact details in Section 13). We will respond within 30 days.",
  ]),
  ("11. Data Retention & Deletion", [
    "Altherix retains personal data only for as long as necessary to fulfill the purposes for which it was collected, unless:",
    ["Required by applicable law or regulation", "Necessary to establish, exercise, or defend legal claims", "Retained for legitimate business purposes with reduced access controls"],
    "Upon deletion, personal data is securely erased or anonymized such that it cannot be reconstructed.",
  ]),
  ("12. Data Breach Notification", [
    "In the event of a data breach that may compromise the rights or freedoms of data subjects, Altherix will:",
    [
      "Promptly notify affected data subjects (without undue delay, where legally required)",
      "Notify relevant regulatory authorities where legally mandated",
      "Provide details of the breach, impact assessment, and mitigation measures",
      "Conduct post-breach investigation and implement corrective actions",
    ],
    "Altherix maintains an incident response plan and breach notification procedures aligned with GDPR and other applicable regulations.",
  ]),
  ("13. Data Protection Officer", [
    "Altherix has appointed a Data Protection Officer (DPO) responsible for overseeing compliance with this policy and applicable data protection laws.",
    "For data privacy inquiries, complaints, or to exercise data subject rights, email <a href=\"mailto:contact@altherix.in?subject=Data%20protection%20request\">contact@altherix.in</a> with the subject &ldquo;Data protection request&rdquo;. Your message goes to the Data Protection Officer.",
  ]),
  ("14. Compliance & Audits", [
    "Altherix complies with all applicable data protection regulations including:",
    [
      "General Data Protection Regulation (GDPR): EU/EEA",
      "Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011: India",
      "Digital Personal Data Protection Act (DPDPA), 2023: India",
      "California Consumer Privacy Act (CCPA) and other US state privacy laws",
    ],
    "Altherix conducts regular audits and assessments to ensure compliance and maintains comprehensive documentation of all processing activities.",
  ]),
  ("15. Policy Updates", [
    "This policy is reviewed annually and updated as necessary to reflect changes in laws, regulations, and best practices. Any material changes will be communicated to data controllers and stakeholders. Continued use of Altherix services constitutes acceptance of the updated policy.",
  ]),
  ("16. Acknowledgment", [
    "By entering into a service agreement with Altherix, clients acknowledge that they have reviewed and understood this Data Privacy &amp; Protection Policy and agree to be bound by its terms.",
  ]),
]
