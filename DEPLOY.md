# Deploy ขึ้น Vercel

โปรเจกต์นี้ deploy เป็น **FastAPI app เดียว** บน Vercel (zero-config): Vercel เจอ `app` ใน `app/main.py` เอง
หน้าเว็บ Astro ถูก build ตอน deploy แล้ว `app.frontend()` ให้ Vercel ย้ายไฟล์ใน `web/dist` ไปเสิร์ฟจาก CDN
ส่วน `/api/*` และ `/cds-services/*` วิ่งเข้า Python function

## ขั้นตอน (ครั้งแรก)

1. Vercel → **Add New… → Project** → import repo นี้ → เลือก branch ที่มีโค้ด (`dev/prototype` หรือหลัง merge)
2. **Root Directory** = root ของ repo (ไม่ใช่ `web/`)
3. **Framework Preset** ควรขึ้น **FastAPI** เอง ถ้าไม่ขึ้น เลือก FastAPI
4. Build / Install command ไม่ต้องแก้ — อยู่ใน `vercel.json` แล้ว
5. **Deploy**

หรือจาก terminal: `npx vercel` (ครั้งแรกจะถามให้ login และ link project) → `npx vercel --prod`

## ไฟล์ที่เกี่ยว

| ไฟล์ | ทำอะไร |
|---|---|
| `vercel.json` | build หน้าเว็บด้วย pnpm 12 ก่อน deploy · ตั้ง function `app/main.py` (timeout 30 วิ, ไม่รวม `node_modules`/tests/docs) |
| `.vercelignore` | ไม่อัปโหลด `.venv`, `node_modules`, ไฟล์ build ในเครื่อง |
| `.python-version` | Python 3.13 |
| `pyproject.toml` + `uv.lock` | dependency ฝั่ง Python (Vercel ใช้ uv ติดตั้งให้) |

## เช็กหลัง deploy

- `/` , `/dashboard/?case=1&visit=2` , `/his/?hn=HN-0001&drug=carbamazepine&dose=200` , `/queue/` เปิดได้
- `/api/eval` และ `/cds-services` ตอบ JSON

## ข้อจำกัดที่ต้องรู้

- **คิวเภสัชกรเก็บในหน่วยความจำของ function** — บน Vercel อาจมีหลาย instance และ instance ถูกปิดเมื่อไม่มีคนใช้
  ตอน demo คนเดียวมักใช้ได้ แต่รายการอาจหายหรือไม่ขึ้นในหน้าคิวเป็นบางครั้ง ถ้าต้องใช้จริง ให้ย้าย `QUEUE` ใน
  `app/cds_hooks.py` ไปเก็บใน Vercel KV / Upstash Redis / Supabase
- ข้อมูลทั้งหมดเป็นข้อมูลจำลอง ลิงก์เป็นสาธารณะ ห้ามใส่ข้อมูลผู้ป่วยจริง
- ทางเลือกถ้าไม่ใช้ Vercel: `Dockerfile` ใช้กับ Render / Fly.io / Hugging Face Spaces ได้
