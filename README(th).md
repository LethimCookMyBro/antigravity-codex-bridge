# Antigravity Codex Bridge

> ชุด skills, agents และ workflows สไตล์ Antigravity ที่แพ็กมาให้ใช้กับ OpenAI Codex

โปรเจกต์นี้ทำขึ้นเพื่อแปลงแนวคิดของ Antigravity Kit ให้อยู่ในรูปแบบที่ **Codex ใช้งานได้จริงผ่านโฟลเดอร์ `.agents`** และสามารถยกไปใช้ต่อในโปรเจกต์อื่นได้ง่าย

## ติดตั้งแบบเร็ว

โคลน repository:

```bash
git clone https://github.com/LethimCookMyBro/antigravity-codex-bridge.git
cd antigravity-codex-bridge
```

ถ้าต้องการเอาไปใช้กับโปรเจกต์อื่น ให้คัดลอกโฟลเดอร์ `.agents` ไปไว้ที่ root ของโปรเจกต์นั้น:

```bash
cp -r .agents /path/to/your-project/
```

ถ้าใช้ Windows PowerShell:

```powershell
Copy-Item -Recurse .agents C:\path\to\your-project\.agents
```

จากนั้นเปิดโปรเจกต์ใน VS Code ที่มี Codex แล้วสั่ง reload skills

## หมายเหตุสำคัญ

repo นี้ออกแบบมาสำหรับ **Codex skills** ไม่ใช่ slash commands ของ Antigravity แบบเดิม

- ใช้ `$brainstorm`, `$debug`, `$plan`, `$create`, `$clean-code`
- ไม่ควรคาดหวัง custom `/brainstorm` หรือ `/debug` ใน Codex
- ควรวางโฟลเดอร์ `.agents/` ไว้ที่ root ของโปรเจกต์ เพื่อให้ Codex มองเห็น skills

## สิ่งที่มีในชุดนี้

| ส่วนประกอบ | จำนวน | รายละเอียด |
|----------|------:|------------|
| **Agents** | 20 | prompt เฉพาะทางสำหรับ frontend, backend, security, QA, DevOps, planning และอื่นๆ |
| **Skills** | 48 | skills ที่ทำให้ใช้กับ Codex ได้จริง และรวม top-level skills จาก Antigravity |
| **Workflows** | 11 | เอกสาร workflow แบบ command-style ที่แปลงเป็น behavior สำหรับ Codex |
| **Scripts** | 4 | helper scripts สำหรับ preview, verification, checklist และ status |

## วิธีใช้งาน

หลังจากคัดลอก `.agents` ไปไว้ในโปรเจกต์แล้ว:

1. เปิดโปรเจกต์ใน VS Code
2. ไปที่แท็บ `CODEX`
3. Reload Window หรือใช้คำสั่ง `Force reload skills`
4. เรียกใช้ skill ด้วย `$`

ตัวอย่าง:

```text
$brainstorm ระบบล็อกอินสำหรับ SaaS dashboard
$create landing page สำหรับคลินิกดูแลผิว
$debug ทำไม login ขึ้น 500
$plan ย้ายระบบจาก REST ไป tRPC
$clean-code รีวิวโมดูลนี้ก่อนปล่อยจริง
$ui-ux-pro-max รีดีไซน์หน้า homepage
```

## Command Skills หลัก

ชุด workflow แบบ Antigravity ที่รวมมาให้:

| Skill | ใช้ทำอะไร |
|-------|------------|
| `$brainstorm` | แตกทางเลือกและคิดก่อนเริ่มลงมือ |
| `$create` | เริ่มสร้างแอปหรือฟีเจอร์ใหม่ |
| `$debug` | ดีบักแบบเป็นระบบ หาต้นตอปัญหา |
| `$deploy` | เช็กก่อน deploy และจัด flow การปล่อยงาน |
| `$enhance` | ปรับปรุงหรือเพิ่มฟีเจอร์ในโปรเจกต์เดิม |
| `$orchestrate` | ประสานหลาย agents สำหรับงานซับซ้อน |
| `$plan` | วางแผนอย่างเดียว ยังไม่เขียนโค้ด |
| `$preview` | จัดการ preview/local server |
| `$status` | ดูสถานะโปรเจกต์และ workflow |
| `$test` | สร้างและรัน tests |
| `$ui-ux-pro-max` | workflow สำหรับงาน UI/UX และ design system |

## Top-Level Skills ที่มีให้

นอกจาก command skills ยังมี skills เฉพาะทางจาก ecosystem ของ Antigravity เช่น:

- `api-patterns`
- `app-builder`
- `architecture`
- `bash-linux`
- `behavioral-modes`
- `brainstorming`
- `clean-code`
- `database-design`
- `documentation-templates`
- `frontend-design`
- `game-development`
- `geo-fundamentals`
- `i18n-localization`
- `intelligent-routing`
- `lint-and-validate`
- `mcp-builder`
- `mobile-design`
- `nodejs-best-practices`
- `parallel-agents`
- `performance-profiling`
- `plan-writing`
- `powershell-windows`
- `python-patterns`
- `react-best-practices`
- `red-team-tactics`
- `rust-pro`
- `seo-fundamentals`
- `server-management`
- `systematic-debugging`
- `tailwind-patterns`
- `tdd-workflow`
- `testing-patterns`
- `vulnerability-scanner`
- `web-design-guidelines`
- `webapp-testing`

## อะไรควร push ขึ้น GitHub

repo นี้ตั้งใจให้ publish เฉพาะแพ็ก Codex ที่พร้อมใช้งาน

ควร push:

- `.agents/`
- `.gitignore`
- `LICENSE`
- `README.md`
- `README(th).md`

ไม่ควร push:

- `.agent/`
- `plugins/antigravity/`
- `.agents/plugins/`

## เป้าหมายของ repo นี้

เป้าหมายคือให้ได้แพ็กแบบ Codex-first ที่สะอาดและหยิบไปใช้ต่อได้ง่าย:

- ไม่มี `.agent` กับ `.agents` ซ้ำกันใน repo ที่ publish
- ไม่ต้องพึ่ง local plugin bridge
- ไม่อ้าง path ภายในเครื่องแบบซ่อนๆ
- เหลือเพียง `.agents` ที่พร้อมใช้กับ Codex

## เครดิต

ได้แรงบันดาลใจจาก Antigravity Kit ต้นฉบับ และนำมาปรับให้ใช้งานกับ Codex เป็นหลัก

## License

MIT
