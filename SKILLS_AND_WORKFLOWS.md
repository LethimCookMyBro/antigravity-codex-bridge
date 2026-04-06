# Skills and Workflows Catalog

Last updated: 2026-04-06

This catalog lists every project-local workflow and skill currently shipped in AG Kit.
Use it as a quick reference when you want to know what each item is for before invoking it in Codex.

Note:
- Workflows are entrypoints under `.agents/workflows/`.
- Skills are guidance/playbooks under `.agents/skills/`.
- This catalog covers project-local items only.

## Workflows (11)

| Name | Purpose |
|---|---|
| `brainstorm` | Structured brainstorming before implementation so the team explores options first. |
| `create` | Start a new application or project build and route the request into the creation workflow. |
| `debug` | Enter a systematic debugging flow for investigation, evidence collection, and root-cause analysis. |
| `deploy` | Run the deployment workflow with pre-flight checks, release steps, and verification. |
| `enhance` | Add or update features in an existing application through an iterative enhancement workflow. |
| `orchestrate` | Coordinate multiple skills or agents for complex work that spans more than one domain. |
| `plan` | Generate a project plan or execution plan before implementation begins. |
| `preview` | Manage the local preview server by starting, stopping, restarting, or checking status. |
| `status` | Show current project, preview, and task progress status. |
| `test` | Generate, run, and review tests for the current code or feature. |
| `ui-ux-pro-max` | Trigger the advanced UI/UX design workflow for redesign, exploration, and systemized visual work. |

## Skills (106)

| Name | Purpose |
|---|---|
| `adversarial-emulation` | Translate defensive findings into ATT&CK-aligned detection validation and purple-team planning without operational payload guidance. |
| `ai-incident-log-analysis` | Use structured AI-assisted log analysis for incident response, IOC extraction, and triage summaries with a local helper script. |
| `ai-research` | Review AI-system security posture across prompts, RAG, connectors, models, and governance with safe research outputs. |
| `api-patterns` | API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination. |
| `app-builder` | Main application building orchestrator. Creates full-stack applications from natural language requests. Determines project type, selects tech stack, coordinates agents. |
| `app-builder/templates` | Project scaffolding templates for new applications. Use when creating new projects from scratch. Contains 12 templates for various tech stacks. |
| `architecture` | Architectural decision-making framework. Requirements analysis, trade-off evaluation, ADR documentation. Use when making architecture decisions or analyzing system design. |
| `auth-log-triage` | Triage Linux authentication logs with grep, awk, and Python parsers to correlate users, failures, source IPs, and sudo activity. |
| `bash-linux` | Bash/Linux terminal patterns. Critical commands, piping, error handling, scripting. Use when working on macOS or Linux systems. |
| `behavioral-modes` | AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type. |
| `brainstorm` | Structured brainstorming for projects and features. Explores multiple options before implementation. |
| `brainstorming` | Socratic questioning protocol + user communication. MANDATORY for complex requests, new features, or unclear requirements. Includes progress reporting and error handling. |
| `buffer-overflow-examples` | Review memory-safety concepts, crash evidence, and secure remediation patterns without exploit weaponization. |
| `bug-bounties` | Review scope notes, target inventory, evidence handling, and report-quality workflows for authorized bug bounty programs. |
| `capture-the-flag` | Structured CTF challenge workflow for local or hosted labs. Triage artifacts, classify challenge type, and build a safe solving plan. |
| `car-hacking` | Review automotive lab assets, buses, firmware evidence, and safe defensive validation boundaries in owned labs. |
| `cheat-sheets` | Quick-reference operational patterns for safe evidence collection, validation, and reporting across defensive skill workflows. |
| `clean-code` | Pragmatic coding standards - concise, direct, no over-engineering, no unnecessary comments |
| `cloud-resources` | Review cloud exposure, logging posture, ownership signals, and service security evidence across AWS, Azure, and GCP with low-noise validation. |
| `code-review-checklist` | Code review guidelines covering code quality, security, and best practices. |
| `cracking-passwords` | Defensive password-hash triage. Identify hash types, storage characteristics, and remediation needs without attempting password recovery or providing cracking workflows. |
| `create` | Create new application command. Triggers App Builder skill and starts interactive dialogue with user. |
| `cryptography-and-pki` | Review key handling, certificate workflows, TLS posture, and PKI hygiene with practical OpenSSL-based validation and local helper scripts. |
| `darkweb-research` | Document safe research handling, keyword tracking, and evidence hygiene for threat monitoring without participating in illicit activity. |
| `database-design` | Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases. |
| `debug` | Debugging command. Activates DEBUG mode for systematic problem investigation. |
| `deploy` | Deployment command for production releases. Pre-flight checks and deployment execution. |
| `deployment-procedures` | Production deployment principles and decision-making. Safe deployment workflows, rollback strategies, and verification. Teaches thinking, not scripts. |
| `devsecops` | Review CI/CD, dependencies, secrets, and deployment automation with evidence-first security checks for owned repositories and pipelines. |
| `dfir` | Perform defensive digital forensics and incident response triage across logs, pcaps, host artifacts, and timelines using low-noise evidence collection patterns. |
| `dns-ownership-recon` | Resolve DNS, gather MX/NS/TXT context, enrich with whois ownership, and flag likely cloud hosting with a local helper script. |
| `docker-and-k8s-security` | Review Docker and Kubernetes configuration, workload exposure, and manifest risk with evidence-first defensive checks. |
| `documentation-templates` | Documentation templates and structure guidelines. README, API docs, code comments, and AI-friendly documentation. |
| `enhance` | Add or update features in existing application. Used for iterative development. |
| `exploit-development` | Safe root-cause and reproduction-boundary review for confirmed vulnerabilities. Do not produce weaponized exploits, payloads, or bypass steps. |
| `foundational-cybersecurity-concepts` | Explain core defensive concepts, terminology, and decision rules that support deeper security skills. |
| `frontend-design` | Design thinking and decision-making for web UI. Use when designing components, layouts, color schemes, typography, or creating aesthetic interfaces. Teaches principles, not fixed values. |
| `fuzzing-resources` | Plan safe fuzzing, crash triage, corpus management, and remediation review in owned test environments. |
| `game-development/2d-games` | 2D game development principles. Sprites, tilemaps, physics, camera. |
| `game-development/3d-games` | 3D game development principles. Rendering, shaders, physics, cameras. |
| `game-development` | Game development orchestrator. Routes to platform-specific skills based on project needs. |
| `game-development/game-art` | Game art principles. Visual style selection, asset pipeline, animation workflow. |
| `game-development/game-audio` | Game audio principles. Sound design, music integration, adaptive audio systems. |
| `game-development/game-design` | Game design principles. GDD structure, balancing, player psychology, progression. |
| `game-development/mobile-games` | Mobile game development principles. Touch input, battery, performance, app stores. |
| `game-development/multiplayer` | Multiplayer game development principles. Architecture, networking, synchronization. |
| `game-development/pc-games` | PC and console game development principles. Engine selection, platform features, optimization strategies. |
| `game-development/vr-ar` | VR/AR development principles. Comfort, interaction, performance requirements. |
| `game-development/web-games` | Web browser game development principles. Framework selection, WebGPU, optimization, PWA. |
| `game-hacking` | Review anti-tamper, client trust boundaries, telemetry, and lab-only integrity testing for owned games. |
| `geo-fundamentals` | Generative Engine Optimization for AI search engines (ChatGPT, Claude, Perplexity). |
| `h4cker-skill-architect` | Distill dense h4cker folders into compact, high-signal Codex skills without pushing the raw source. |
| `honeypots-honeynets` | Deploy and review deception infrastructure, telemetry quality, and containment boundaries for defensive monitoring. |
| `i18n-localization` | Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support. |
| `intelligent-routing` | Automatic agent selection and intelligent task routing. Analyzes user requests and automatically selects the best specialist agent(s) without requiring explicit user mentions. |
| `iot-hacking` | Authorized IoT and OT exposure review for owned devices and industrial endpoints. Focus on identification, protocol inventory, and hardening evidence. |
| `lint-and-validate` | Automatic quality control, linting, and static analysis procedures. Use after every code modification to ensure syntax correctness and project standards. Triggers onKeywords: lint, format, check, validate, types, static analysis. |
| `linux-hardening` | Harden Linux systems with evidence-based checks for compromise, firewall posture, system integrity, privilege exposure, and log visibility. |
| `mcp-builder` | MCP (Model Context Protocol) server building principles. Tool design, resource patterns, best practices. |
| `metasploit-resources` | Document framework hygiene, module review, and defensive validation boundaries without operational exploit steps. |
| `methodology` | Build a scoped security assessment plan with phase gates, evidence requirements, and clean handoffs between recon, testing, and defensive review. |
| `mobile-design` | Mobile-first design thinking and decision-making for iOS and Android apps. Touch interaction, performance patterns, platform conventions. Teaches principles, not fixed values. Use when building React Native, Flutter, or native mobile apps. |
| `mobile-security` | Review mobile app packaging, storage, transport, and permission posture for owned Android or iOS applications. |
| `networking` | Review owned network layout, service exposure, DNS context, and packet evidence with low-noise enumeration and local helper scripts. |
| `nodejs-best-practices` | Node.js development principles and decision-making. Framework selection, async patterns, security, and architecture. Teaches thinking, not copying. |
| `orchestrate` | Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise. |
| `osint` | Public-source intelligence gathering for domains, identities, documents, and relationships with clean evidence and downstream handoff. |
| `osint-recon` | Authorized passive reconnaissance and controlled surface validation for domains, identities, exposed services, and public web assets. |
| `packet-capture-lab` | Use Scapy and PyShark for authorized packet capture, pcap inspection, protocol debugging, and tightly scoped network validation in labs or owned environments. |
| `parallel-agents` | Multi-agent orchestration patterns. Use when multiple independent tasks can run with different domain expertise or when comprehensive analysis requires multiple perspectives. |
| `pen-testing-reports` | Structure evidence-first findings, remediation notes, and executive summaries for authorized testing engagements. |
| `performance-profiling` | Performance profiling principles. Measurement, analysis, and optimization techniques. |
| `plan` | Create project plan using project-planner agent. No code writing, only plan file generation. |
| `plan-writing` | Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work. |
| `post-exploitation` | Defensive impact mapping after an assumed foothold. No persistence, lateral movement, evasion, or operator playbooks. |
| `powershell-windows` | PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling. |
| `preview` | Preview server start, stop, and status check. Local development server management. |
| `programming-and-scripting-for-cybersecurity` | Implement small defensive helper scripts and parsing patterns after a primary security skill has already defined the target, scope, and evidence goal. |
| `python-patterns` | Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying. |
| `python-ruby-and-bash` | Choose simple scripting patterns for defensive automation, parsing, and reproducible system checks after the main security objective is already scoped. |
| `react-best-practices` | React and Next.js performance optimization from Vercel Engineering. Use when building React components, optimizing performance, eliminating waterfalls, reducing bundle size, reviewing code for performance issues, or implementing server/client-side optimizations. |
| `recon` | Authorized low-noise reconnaissance router. Build a scoped target inventory, preserve evidence, and hand off clean inputs to web application testing. |
| `red-team-tactics` | Red team tactics principles based on MITRE ATT&CK. Attack phases, detection evasion, reporting. |
| `reverse-engineering` | Static and controlled dynamic analysis of owned or challenge binaries. Focus on understanding behavior and artifacts, not malware development. |
| `rust-pro` | Master Rust 1.75+ with modern async patterns, advanced type system |
| `sbom` | Build and review software bill of materials evidence, lockfiles, and package manifests for supply-chain visibility in owned projects. |
| `seo-fundamentals` | SEO fundamentals, E-E-A-T, Core Web Vitals, and Google algorithm principles. |
| `server-management` | Server management principles and decision-making. Process management, monitoring strategy, and scaling decisions. Teaches thinking, not commands. |
| `social-engineering` | Defensive social-engineering risk review. Analyze trust surfaces and awareness gaps without crafting lures, impersonation, or deceptive campaign content. |
| `status` | Display agent and project status. Progress tracking and status board. |
| `systematic-debugging` | 4-phase systematic debugging methodology with root cause analysis and evidence-based verification. Use when debugging complex issues. |
| `tailwind-patterns` | Tailwind CSS v4 principles. CSS-first configuration, container queries, modern patterns, design token architecture. |
| `tdd-workflow` | Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle. |
| `test` | Test generation and test running command. Creates and executes tests for code. |
| `testing-patterns` | Testing patterns and principles. Unit, integration, mocking strategies. |
| `threat-hunting` | Defensive threat-hunting workflow for hypotheses, pivots, evidence correlation, and artifact-ready outputs. |
| `threat-intelligence` | Enrich domains, IPs, accounts, and incident artifacts with defensive context, ownership evidence, and IOC grouping for authorized analysis. |
| `tls-cert-audit` | Inspect certificate metadata, negotiated TLS details, and weak-crypto acceptance with a local helper script for owned or authorized hosts. |
| `ui-ux-pro-max` | AI-powered design intelligence with 50+ styles, 95+ color palettes, and automated design system generation. |
| `vulnerability-scanner` | Advanced vulnerability analysis principles. OWASP 2025, Supply Chain Security, attack surface mapping, risk prioritization. |
| `vulnerable-servers` | Track lab server purpose, safe validation scope, patch gaps, and containment controls for intentionally vulnerable environments. |
| `web-application-testing` | Authorized web application review using scoped inventory, low-noise validation, and evidence-first findings that can hand off to deeper root-cause analysis. |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices". |
| `webapp-testing` | Web application testing principles. E2E, Playwright, deep audit strategies. |
| `windows` | Review Windows host posture, services, firewall, logs, and scheduled persistence with defensive evidence-first commands. |
| `wireless-resources` | Document authorized wireless inventory, signal baseline, and defensive monitoring steps in owned environments. |
