# AG Kit

ชุด skills, specialist agents, workflows และ helper scripts แบบพกพาสำหรับ OpenAI Codex ในแพ็กเดียว

`@lizmotia/ag-kit` ใช้สำหรับติดตั้งโฟลเดอร์ `.agents` ลงในโปรเจกต์ เพื่อให้ Codex มองเห็นชุดการทำงานเดียวกันได้ในทุก repo

## ติดตั้ง

รันในโปรเจกต์ปลายทางได้เลย:

```bash
npx @lizmotia/ag-kit init
```

หรือติดตั้งแบบ global:

```bash
npm install -g @lizmotia/ag-kit
ag-kit init
```

ถ้าต้องการอัปเดตของเดิมที่ติดตั้งไว้แล้ว:

```bash
npx @lizmotia/ag-kit update
```

ถ้าจะใช้ `init` แล้วเขียนทับ `.agents` เดิมโดยตรง ก็ทำได้:

```bash
npx @lizmotia/ag-kit init --force
```

ถ้าจะทดสอบจาก source ใน repo นี้:

```bash
node ./bin/ag-codex.js init --path ../my-project
```

alias ที่ยังใช้ได้:

```bash
ag-codex init
```

## แพ็กนี้ติดตั้งอะไรให้

CLI จะคัดลอก `.agents` แบบพกพาไปไว้ที่ root ของโปรเจกต์ปลายทาง

ชุดที่ติดตั้งตอนนี้มี:

| ส่วนประกอบ | จำนวน | หน้าที่ |
|---------|------:|---------|
| Agents | 20 | บทบาทเฉพาะทาง เช่น frontend, backend, security, QA และ planning |
| Skills | 96 top-level / 106 ไฟล์ SKILL ทั้งหมด | คำสั่งนำทาง, playbook, checklist และแนวปฏิบัติสำหรับ Codex |
| Workflows | 11 | entry workflow เช่น `brainstorm`, `create`, `debug`, `plan` และ `test` |
| Scripts | 17 | helper สำหรับ verification, stale check, health check, load order, preview, checklist และ session |

## แนวคิดหลัก

AG Kit ถูกออกแบบมาสำหรับระบบ skills ของ Codex ไม่ใช่ runtime ของ slash commands แบบ custom

- ใช้ `$brainstorm`, `$create`, `$debug`, `$plan`, `$test` และ skill อื่น ๆ ภายใน Codex
- วาง `.agents/` ไว้ที่ root ของโปรเจกต์ เพื่อให้ Codex หาเจอ
- ใช้แพ็กเดียวเพื่อลดการคัดลอก prompts และ helper files ซ้ำ ๆ ระหว่างหลาย repo

## ลำดับการใช้งานทั่วไป

1. ติดตั้ง `.agents` ลงในโปรเจกต์
2. เปิดโปรเจกต์นั้นใน VS Code
3. ไปที่แท็บ `CODEX`
4. Reload window หรือใช้ `Force reload skills`
5. เรียกใช้งานด้วย `$`

ตัวอย่าง:

```text
$brainstorm ระบบล็อกอินสำหรับ SaaS dashboard
$create landing page สำหรับคลินิกดูแลผิว
$debug ทำไม login ขึ้น 500
$plan ย้ายระบบจาก REST ไป tRPC
$clean-code รีวิวโมดูลนี้ก่อนปล่อยจริง
$ui-ux-pro-max รีดีไซน์หน้า homepage
```

ถ้ามีคน clone repo นี้ตรง ๆ อยู่แล้ว ก็ไม่ต้อง install เพิ่มเพื่อใช้ใน repo นี้ เพราะ `.agents/` อยู่ในโปรเจกต์แล้ว ให้ทำแค่นี้:

1. เปิด root ของ repo ใน VS Code
2. ไปที่แท็บ `CODEX`
3. Reload window หรือใช้ `Force reload skills`
4. เรียกใช้ skill ด้วย `$`

## CLI

| คำสั่ง | ใช้ทำอะไร |
|---------|------------|
| `ag-kit init` | ติดตั้ง `.agents` ลงในโฟลเดอร์ปัจจุบัน |
| `ag-kit init --path ./my-project` | ติดตั้งลงใน path ที่ระบุ |
| `ag-kit update` | ติดตั้งซ้ำและเขียนทับ `.agents` เดิม |
| `ag-kit init --force` | เขียนทับ `.agents` เดิมระหว่างใช้ `init` |
| `ag-kit status` | เช็กว่าติดตั้งแล้วหรือยังและสรุปจำนวนไฟล์หลัก |
| `ag-kit help` | แสดงวิธีใช้งาน |

## ชื่อ package บน npm

แพ็กที่ publish อยู่ตอนนี้คือ:

```bash
@lizmotia/ag-kit
```

ใน repo ยังเก็บ `ag-codex` ไว้เป็น alias เพื่อความเข้ากันได้ แต่ชื่อหลักที่ควรใช้ต่อจากนี้คือ `ag-kit`

## การอัปเดตโปรเจกต์ที่ติดตั้งไว้แล้ว

ถ้าโปรเจกต์มี `.agents` อยู่แล้วและต้องการอัปเดตเป็นเวอร์ชันล่าสุด ให้ใช้:

```bash
npx @lizmotia/ag-kit update
```

ถ้าเพิ่ง publish เวอร์ชันใหม่และอยากกันปัญหา `npx` cache ค้าง ให้ใช้:

```bash
npx @lizmotia/ag-kit@latest update
```

ถ้าติดตั้งแบบ global:

```bash
ag-kit update
```

`init --force` ก็ใช้ได้ แต่ `update` จะสื่อความหมายตรงกว่า เพราะบอกชัดว่าเป็นการ refresh ของเดิม

## โครงสร้าง repo

```text
.
|-- .agents/
|   |-- agents/
|   |-- skills/
|   |-- workflows/
|   |-- scripts/
|   `-- .shared/
|-- bin/ag-codex.js
|-- AGENT_FLOW.md
|-- PUBLISHING.md
|-- SKILLS_AND_WORKFLOWS.md
|-- SKILLS_AND_WORKFLOWS_TH.md
|-- README.md
`-- README(th).md
```

## ขอบเขตที่ถูก publish

แพ็กบน npm ตั้งใจให้มีเฉพาะ runtime แบบพกพาที่จำเป็น:

- `.agents/`
- `bin/`
- `AGENT_FLOW.md`
- `PUBLISHING.md`
- `UPDATELIST.md`
- `SKILLS_AND_WORKFLOWS.md`
- `SKILLS_AND_WORKFLOWS_TH.md`
- `README.md`
- `README(th).md`
- `LICENSE`
- `package.json`

ไฟล์ compatibility ที่ใช้เฉพาะในเครื่องหรือในสภาพแวดล้อมพัฒนา จะไม่ถูกรวมไปในแพ็กที่ publish

## หมายเหตุสำหรับการ push ขึ้น GitHub

ไฟล์ที่ควร push:

- `.agents/`
- `bin/`
- `README.md`
- `README(th).md`
- `UPDATELIST.md`
- `SKILLS_AND_WORKFLOWS.md`
- `SKILLS_AND_WORKFLOWS_TH.md`
- `AGENT_FLOW.md`
- `PUBLISHING.md`
- `LICENSE`
- `package.json`
- `.npmignore`

ไฟล์ที่ควรเป็น local-only:

- `.agent/`
- `plugins/`
- `.agents/plugins/`
- `h4cker/`
- `awesome-design-md/`
- รายงาน audit หรือ scratch docs ที่ใช้เฉพาะตอนพัฒนา

## เอกสารเพิ่มเติม

- [Agent Flow](./AGENT_FLOW.md)
- [Publishing Guide](./PUBLISHING.md)
- [Update List](./UPDATELIST.md)
- [Skills and Workflows Catalog](./SKILLS_AND_WORKFLOWS.md)
- [สารบัญ Skills และ Workflows](./SKILLS_AND_WORKFLOWS_TH.md)

## License

MIT
