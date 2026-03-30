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
| Skills | 48 | คำสั่งนำทาง, playbook, checklist และแนวปฏิบัติสำหรับ Codex |
| Workflows | 11 | entry workflow เช่น `brainstorm`, `create`, `debug`, `plan` และ `test` |
| Scripts | 4 | helper สำหรับ verification, preview, checklist และ session |

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

## CLI

| คำสั่ง | ใช้ทำอะไร |
|---------|------------|
| `ag-kit init` | ติดตั้ง `.agents` ลงในโฟลเดอร์ปัจจุบัน |
| `ag-kit init --path ./my-project` | ติดตั้งลงใน path ที่ระบุ |
| `ag-kit update` | ติดตั้งซ้ำและเขียนทับ `.agents` เดิม |
| `ag-kit status` | เช็กว่าติดตั้งแล้วหรือยังและสรุปจำนวนไฟล์หลัก |
| `ag-kit help` | แสดงวิธีใช้งาน |

## ชื่อ package บน npm

แพ็กที่ publish อยู่ตอนนี้คือ:

```bash
@lizmotia/ag-kit
```

ใน repo ยังเก็บ `ag-codex` ไว้เป็น alias เพื่อความเข้ากันได้ แต่ชื่อหลักที่ควรใช้ต่อจากนี้คือ `ag-kit`

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
|-- README.md
`-- README(th).md
```

## ขอบเขตที่ถูก publish

แพ็กบน npm ตั้งใจให้มีเฉพาะ runtime แบบพกพาที่จำเป็น:

- `.agents/`
- `bin/`
- `AGENT_FLOW.md`
- `PUBLISHING.md`
- `README.md`
- `README(th).md`
- `LICENSE`
- `package.json`

ไฟล์ compatibility ที่ใช้เฉพาะในเครื่องหรือในสภาพแวดล้อมพัฒนา จะไม่ถูกรวมไปในแพ็กที่ publish

## เอกสารเพิ่มเติม

- [Agent Flow](./AGENT_FLOW.md)
- [Publishing Guide](./PUBLISHING.md)

## License

MIT
