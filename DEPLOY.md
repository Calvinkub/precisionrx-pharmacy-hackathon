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

- `/` , `/overview/` , `/metabolomics/` , `/molecular/` , `/action-plan/` เปิดได้
- `/api/eval` และ `/cds-services` ตอบ JSON

## Claude (ถ้าต้องการ)

ตั้ง Environment Variable `ANTHROPIC_API_KEY` ใน Vercel Project Settings → API `/api/v2/patients/{id}/run` จะใช้ Claude วางแผนและเรียบเรียงสรุป
ถ้าไม่ตั้ง ระบบใช้ template ที่ให้ผลเหมือนเดิมทุกครั้ง (ทุกอย่างยังใช้ได้)

## ข้อจำกัดที่ต้องรู้

- WebSocket (`/ws/...`) ใช้ไม่ได้บน Vercel — หน้าเว็บถอยไปใช้ REST เอง จึงไม่เห็น progress ทีละขั้นระหว่างรัน

- ทุกหน้าไม่เก็บ state ฝั่ง server (ข้อมูลผู้ป่วยที่แก้เก็บใน sessionStorage ของเบราว์เซอร์) จึงเหมาะกับ serverless
- ผลตรวจที่อัปโหลด CSV อยู่แค่ในหน้านั้น ไม่ถูกบันทึก
- ข้อมูลทั้งหมดเป็นข้อมูลจำลอง ลิงก์เป็นสาธารณะ ห้ามใส่ข้อมูลผู้ป่วยจริง
- ทางเลือกถ้าไม่ใช้ Vercel: `Dockerfile` ใช้กับ Render / Fly.io / Hugging Face Spaces ได้
