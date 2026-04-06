# สารบัญ Skills และ Workflows

อัปเดตล่าสุด: 2026-04-06

ไฟล์นี้สรุปรายการ workflows และ skills ที่มีอยู่จริงใน AG Kit เวอร์ชันปัจจุบัน
เพื่อให้เปิดดูได้เร็วว่าแต่ละอันเอาไว้ทำอะไร ก่อนเรียกใช้ใน Codex

หมายเหตุ:
- Workflows คือ entrypoints ใต้ `.agents/workflows/`
- Skills คือคู่มือ/แนวทางการทำงานใต้ `.agents/skills/`
- ไฟล์นี้รวมเฉพาะรายการที่อยู่ในโปรเจกต์นี้

## Workflows (11)

| ชื่อ | ใช้ทำอะไร |
|---|---|
| `brainstorm` | ใช้เริ่มระดมไอเดียก่อนลงมือทำ เพื่อสำรวจทางเลือกให้รอบด้านก่อน |
| `create` | ใช้เริ่มสร้างแอปหรือโปรเจกต์ใหม่ และส่งงานเข้ากระบวนการสร้างโปรเจกต์ |
| `debug` | ใช้เปิดโหมด debug แบบเป็นระบบ เพื่อสืบหาสาเหตุและเก็บหลักฐาน |
| `deploy` | ใช้ทำ workflow สำหรับปล่อยขึ้นระบบจริง พร้อมเช็กก่อนปล่อยและยืนยันผล |
| `enhance` | ใช้เพิ่มหรือปรับปรุงฟีเจอร์ในโปรเจกต์เดิมแบบ iterative |
| `orchestrate` | ใช้ประสานหลาย skills หรือหลาย agents สำหรับงานที่ซับซ้อนหลายด้าน |
| `plan` | ใช้สร้างแผนงานหรือ execution plan ก่อนเริ่ม implement |
| `preview` | ใช้จัดการ local preview server เช่น start, stop, restart และ status |
| `status` | ใช้ดูสถานะงาน โปรเจกต์ preview และความคืบหน้าปัจจุบัน |
| `test` | ใช้สร้าง รัน และตรวจผล tests ของโค้ดหรือฟีเจอร์ปัจจุบัน |
| `ui-ux-pro-max` | ใช้เรียก workflow ออกแบบ UI/UX ขั้นสูงสำหรับ redesign และงาน visual system |

## Skills (106)

| ชื่อ | ใช้ทำอะไร |
|---|---|
| `adversarial-emulation` | ใช้แปลง findings เชิงป้องกันเป็นแผนตรวจจับและ purple-team validation |
| `ai-incident-log-analysis` | ใช้วิเคราะห์ log incident ด้วย AI เพื่อดึง IOC และสรุป triage |
| `ai-research` | ใช้ตรวจความปลอดภัยของระบบ AI เช่น prompts, RAG, connectors และ governance |
| `api-patterns` | ใช้เลือกและออกแบบรูปแบบ API เช่น REST, GraphQL, tRPC, versioning และ pagination |
| `app-builder` | ใช้สร้างแอปเต็มระบบจาก requirement และประสาน agent ที่เกี่ยวข้อง |
| `app-builder/templates` | ใช้เลือก template โปรเจกต์เริ่มต้นตาม stack ที่ต้องการ |
| `architecture` | ใช้วิเคราะห์สถาปัตยกรรม ระบบ trade-off และ ADR |
| `auth-log-triage` | ใช้ triage auth logs บน Linux เพื่อดู user, source IP, failures และ sudo activity |
| `bash-linux` | ใช้แนวทางคำสั่งและ scripting บน Bash/Linux |
| `behavioral-modes` | ใช้ปรับโหมดการทำงานของ AI ตามประเภทงาน เช่น brainstorm, debug, review |
| `brainstorm` | ใช้ระดมไอเดียอย่างเป็นโครงสร้างก่อนลงมือทำ |
| `brainstorming` | ใช้ถามนำและ clarify requirement สำหรับงานที่ซับซ้อนหรือกำกวม |
| `buffer-overflow-examples` | ใช้ทบทวน crash และ memory-safety แบบไม่ไปทาง weaponize |
| `bug-bounties` | ใช้จัดการ scope, evidence และการเขียนรายงานสำหรับ bug bounty แบบได้รับอนุญาต |
| `capture-the-flag` | ใช้จัดหมวด challenge CTF และวางแผนแก้แบบเป็นระบบ |
| `car-hacking` | ใช้ตรวจ asset, bus, firmware และขอบเขต validation ของระบบยานยนต์ใน lab |
| `cheat-sheets` | ใช้เป็นคู่มือคำสั่งย่อสำหรับเก็บ evidence, validation และ reporting |
| `clean-code` | ใช้รีวิวความสะอาดของโค้ดให้กระชับและไม่ over-engineer |
| `cloud-resources` | ใช้ตรวจ exposure, logging และ security evidence บน AWS, Azure และ GCP |
| `code-review-checklist` | ใช้ checklist review คุณภาพและความปลอดภัยของโค้ด |
| `cracking-passwords` | ใช้ triage hash เชิงป้องกัน ระบุชนิดและความเสี่ยง โดยไม่กู้รหัสผ่าน |
| `create` | ใช้เริ่มสร้างโปรเจกต์หรือแอปใหม่ผ่าน App Builder |
| `cryptography-and-pki` | ใช้ตรวจ key handling, TLS, certificates และสุขอนามัย PKI |
| `darkweb-research` | ใช้ทำ threat research แบบปลอดภัยโดยไม่เข้าไปมีส่วนร่วมกับกิจกรรมผิดกฎหมาย |
| `database-design` | ใช้ตัดสินใจเรื่อง schema, index, ORM และ database architecture |
| `debug` | ใช้เปิดโหมด debug แบบเป็นระบบ |
| `deploy` | ใช้เตรียมและทำ deployment พร้อม pre-flight checks |
| `deployment-procedures` | ใช้คิดเรื่อง deploy, rollback และ verification อย่างปลอดภัย |
| `devsecops` | ใช้ตรวจ CI/CD, dependencies, secrets และ pipeline security |
| `dfir` | ใช้ทำ digital forensics และ incident response triage |
| `dns-ownership-recon` | ใช้ดู DNS, ownership และ cloud clues ของโดเมน |
| `docker-and-k8s-security` | ใช้ตรวจความเสี่ยงของ Docker, Kubernetes และ manifest exposure |
| `documentation-templates` | ใช้ template เอกสาร เช่น README, API docs และ code comments |
| `enhance` | ใช้เพิ่มหรือปรับฟีเจอร์ในโปรเจกต์เดิม |
| `exploit-development` | ใช้วิเคราะห์ root cause และขอบเขตการ reproduce แบบไม่ weaponize |
| `foundational-cybersecurity-concepts` | ใช้อธิบาย concept และคำศัพท์พื้นฐานด้าน cyber defense |
| `frontend-design` | ใช้คิดงานออกแบบหน้าเว็บ, layout, color, typography และ UX |
| `fuzzing-resources` | ใช้วางแผน fuzzing แบบปลอดภัย, triage crash และจัดการ corpus |
| `game-development/2d-games` | ใช้หลักการพัฒนาเกม 2D เช่น sprites, tilemaps และ camera |
| `game-development/3d-games` | ใช้หลักการพัฒนาเกม 3D เช่น rendering, shaders และ physics |
| `game-development` | ใช้เป็นตัว orchestrate งานพัฒนาเกมและ route ไป skill ย่อย |
| `game-development/game-art` | ใช้วางแนวทาง game art, style และ asset pipeline |
| `game-development/game-audio` | ใช้วางระบบเสียงและดนตรีในเกม |
| `game-development/game-design` | ใช้หลักการออกแบบเกม, balancing และ progression |
| `game-development/mobile-games` | ใช้หลักการพัฒนาเกมมือถือ |
| `game-development/multiplayer` | ใช้หลักการออกแบบระบบ multiplayer และ synchronization |
| `game-development/pc-games` | ใช้หลักการพัฒนาเกม PC และ console |
| `game-development/vr-ar` | ใช้หลักการพัฒนา VR/AR |
| `game-development/web-games` | ใช้หลักการพัฒนาเกมบนเว็บ, PWA และ WebGPU |
| `game-hacking` | ใช้ตรวจ anti-tamper และ trust boundary ของเกมใน lab ของตนเอง |
| `geo-fundamentals` | ใช้ทำ GEO สำหรับ AI search engines อย่าง ChatGPT, Claude และ Perplexity |
| `h4cker-skill-architect` | ใช้สกัดเนื้อหาจาก h4cker ให้เป็น Codex skill ที่กระชับและใช้ได้จริง |
| `honeypots-honeynets` | ใช้ติดตั้งและตรวจ honeypot / honeynet แบบ defensive |
| `i18n-localization` | ใช้ตรวจ i18n/l10n, hardcoded strings และ locale management |
| `intelligent-routing` | ใช้ช่วยเลือก agent หรือ skill ที่เหมาะสมอัตโนมัติ |
| `iot-hacking` | ใช้ตรวจ exposure ของ IoT/OT แบบได้รับอนุญาต เน้น inventory และ hardening evidence |
| `lint-and-validate` | ใช้รัน lint, validation และ static checks หลังแก้โค้ด |
| `linux-hardening` | ใช้ harden Linux และตรวจ posture / compromise indicators |
| `mcp-builder` | ใช้สร้าง MCP servers, tools และ resources อย่างเป็นระบบ |
| `metasploit-resources` | ใช้ทบทวน framework hygiene และขอบเขตการ validation แบบไม่ operational |
| `methodology` | ใช้วาง phase plan, evidence requirements และ handoff ของงาน security review |
| `mobile-design` | ใช้แนวคิดออกแบบ mobile-first สำหรับ iOS และ Android |
| `mobile-security` | ใช้ตรวจ package, storage, transport และ permissions ของแอปมือถือ |
| `networking` | ใช้ตรวจ network layout, exposure, DNS และ packet evidence |
| `nodejs-best-practices` | ใช้หลักปฏิบัติที่ดีสำหรับ Node.js |
| `orchestrate` | ใช้ประสานหลาย agents สำหรับงานซับซ้อน |
| `osint` | ใช้เก็บข่าวกรองจากแหล่งสาธารณะเกี่ยวกับ domain, identity และ document |
| `osint-recon` | ใช้ passive recon แบบได้รับอนุญาตสำหรับ domain, services และ public web assets |
| `packet-capture-lab` | ใช้ Scapy และ PyShark ตรวจ pcap หรือ packet capture ใน lab |
| `parallel-agents` | ใช้วางรูปแบบการทำงานหลาย agent แบบขนาน |
| `pen-testing-reports` | ใช้เขียนรายงาน pentest แบบ evidence-first |
| `performance-profiling` | ใช้วัด วิเคราะห์ และปรับปรุง performance |
| `plan` | ใช้สร้างแผนงานโปรเจกต์โดยไม่เขียนโค้ด |
| `plan-writing` | ใช้แตกงานเป็นขั้นตอน พร้อม dependency และ verification |
| `post-exploitation` | ใช้ทำ impact mapping เชิงป้องกันหลังสมมติว่ามี foothold |
| `powershell-windows` | ใช้แนวทางคำสั่งและ scripting บน PowerShell/Windows |
| `preview` | ใช้ start, stop และ check local preview server |
| `programming-and-scripting-for-cybersecurity` | ใช้ทำ helper scripts และ parser เชิงป้องกันหลัง scope ชัดแล้ว |
| `python-patterns` | ใช้หลักการพัฒนา Python และโครงสร้างโปรเจกต์ |
| `python-ruby-and-bash` | ใช้เลือก pattern scripting ง่ายๆ สำหรับ automation เชิงป้องกัน |
| `react-best-practices` | ใช้ปรับ performance และแนวปฏิบัติ React/Next.js |
| `recon` | ใช้ทำ reconnaissance แบบ low-noise และส่ง target list ต่อให้ web testing |
| `red-team-tactics` | ใช้ทบทวน red-team concepts ตาม ATT&CK ในเชิงหลักการและ reporting |
| `reverse-engineering` | ใช้วิเคราะห์ binary, firmware หรือ challenge แบบ static/dynamic อย่างควบคุม |
| `rust-pro` | ใช้หลักการและ pattern ระดับสูงสำหรับ Rust สมัยใหม่ |
| `sbom` | ใช้สร้างและตรวจ SBOM เพื่อมองเห็น supply-chain inventory |
| `seo-fundamentals` | ใช้หลัก SEO, E-E-A-T และ Core Web Vitals |
| `server-management` | ใช้คิดเรื่อง process, monitoring และ server operations |
| `social-engineering` | ใช้รีวิวความเสี่ยง social engineering ในเชิงป้องกัน |
| `status` | ใช้ดูสถานะโปรเจกต์, agent, preview และ validation |
| `systematic-debugging` | ใช้วิธี debug 4 เฟสอย่างเป็นหลักฐาน |
| `tailwind-patterns` | ใช้หลักการ Tailwind CSS v4 และ design token patterns |
| `tdd-workflow` | ใช้วงจร TDD แบบ red-green-refactor |
| `test` | ใช้สร้างและรัน tests |
| `testing-patterns` | ใช้แนวทาง unit, integration และ mocking tests |
| `threat-hunting` | ใช้ตั้งสมมติฐาน hunt และ pivot หลาย telemetry แบบ defensive |
| `threat-intelligence` | ใช้ enrich IOC, domain, IP และ account ด้วยบริบทเชิงป้องกัน |
| `tls-cert-audit` | ใช้ตรวจ cert, TLS details และ weak crypto acceptance |
| `ui-ux-pro-max` | ใช้ design intelligence ขั้นสูงสำหรับ UI/UX และ design system |
| `vulnerability-scanner` | ใช้แนวคิดวิเคราะห์ vulnerability และจัดลำดับความเสี่ยง |
| `vulnerable-servers` | ใช้จัดการ inventory, scope และ patch gaps ของ intentionally vulnerable labs |
| `web-application-testing` | ใช้รีวิวเว็บแอปแบบ evidence-first และ handoff ต่อไป root-cause review |
| `web-design-guidelines` | ใช้ตรวจ UI ตาม Web Interface Guidelines, accessibility และ UX |
| `webapp-testing` | ใช้แนวคิด E2E, Playwright และ deep audit สำหรับเว็บแอป |
| `windows` | ใช้ตรวจ posture ของ Windows host, services, firewall และ logs |
| `wireless-resources` | ใช้ตรวจ inventory และ monitoring ของระบบ wireless แบบได้รับอนุญาต |
