# Antigravity Codex Bridge

ชุด skills, agents และ workflows สไตล์ Antigravity ที่แพ็กมาให้ใช้กับ OpenAI Codex

repo นี้ช่วยติดตั้งชุด `.agents` แบบพกพาเข้าไปในโปรเจกต์ใดก็ได้ เพื่อให้ Codex มองเห็น workflows, specialist agents และ scripts ชุดเดียวกันในแต่ละโปรเจกต์

## มันคืออะไร

- แพ็กแบบ Codex-first สำหรับ repo-local skills และ agents
- CLI ขนาดเล็กสำหรับติดตั้ง `.agents` ลงในโปรเจกต์ปลายทาง
- ตัว bridge สำหรับ workflow แบบ Antigravity เช่น `$brainstorm`, `$debug`, `$plan` และ `$create`

## หมายเหตุสำคัญ

แพ็กนี้ถูกทำมาสำหรับ Codex skills ไม่ใช่ Antigravity slash commands

- ใช้ `$brainstorm`, `$debug`, `$plan`, `$create`, `$clean-code` และ skills อื่น ๆ
- ไม่ควรคาดหวัง custom `/brainstorm` หรือ `/debug` ใน Codex
- ควรวาง `.agents/` ไว้ที่ root ของโปรเจกต์ เพื่อให้ Codex มองเห็น

## เริ่มใช้งานเร็ว

ตราบใดที่ package นี้ยังไม่ได้ publish ขึ้น npm ให้ใช้ local CLI ไปก่อน

รันจาก repo นี้:

```bash
node ./bin/ag-codex.js init --path ../my-project
```

รันจากโปรเจกต์ปลายทาง ในกรณีที่ repo นี้อยู่ข้าง ๆ กัน:

```bash
node ../antigravity-codex-bridge/bin/ag-codex.js init --path .
```

ตัวอย่างบน Windows `cmd`:

```bat
node "..\antigravity-codex-bridge\bin\ag-codex.js" init --path .
```

หลังจาก publish ขึ้น npm แล้ว:

```bash
npx antigravity-codex-bridge init
```

หรือติดตั้งแบบ global:

```bash
npm install -g antigravity-codex-bridge
ag-codex init
```

## หลังติดตั้งแล้วทำอะไรต่อ

1. เปิดโปรเจกต์ปลายทางใน VS Code
2. ไปที่แท็บ `CODEX`
3. Reload window หรือใช้ `Force reload skills`
4. เรียกใช้ skills ด้วย `$`

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
|--------|------------|
| `ag-codex init` | ติดตั้ง `.agents` ลงในโปรเจกต์ปัจจุบัน |
| `ag-codex init --path ./my-project` | ติดตั้งลงใน path ที่ระบุ |
| `ag-codex update` | ติดตั้งซ้ำและเขียนทับ `.agents` เดิม |
| `ag-codex status` | เช็กว่าติดตั้ง `.agents` แล้วหรือยัง และสรุปจำนวนไฟล์หลัก |

## สิ่งที่มีในแพ็กนี้

| ส่วนประกอบ | จำนวน | รายละเอียด |
|----------|------:|------------|
| **Agents** | 20 | prompt เฉพาะทางสำหรับ planning, frontend, backend, security, QA, DevOps และอื่น ๆ |
| **Skills** | 48 | skills ที่ปรับให้ใช้กับ Codex ได้จริง และขยายจาก ecosystem ของ Antigravity |
| **Workflows** | 11 | entrypoints สำหรับงานอย่าง `brainstorm`, `debug`, `plan` และ `test` |
| **Scripts** | 4 | helper scripts สำหรับ preview, verification, checklist และ session |

workflow skills เด่น ๆ:

- `$brainstorm`
- `$create`
- `$debug`
- `$deploy`
- `$enhance`
- `$orchestrate`
- `$plan`
- `$preview`
- `$status`
- `$test`
- `$ui-ux-pro-max`

## เอกสารใน repo

- [Agent Flow Architecture](./AGENT_FLOW.md)

## ขอบเขตที่ควร publish

repo นี้ตั้งใจให้ publish เฉพาะแพ็ก Codex ที่พกพาไปใช้ต่อได้

ควรรวม:

- `.agents/`
- `bin/`
- `.gitignore`
- `.npmignore`
- `LICENSE`
- `README.md`
- `README(th).md`
- `package.json`

ไม่ควรรวมส่วนที่เป็น local-only compatibility:

- `.agent/`
- `plugins/antigravity/`
- `.agents/plugins/`

## License

MIT
