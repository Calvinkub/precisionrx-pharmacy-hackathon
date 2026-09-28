// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

const API = "http://localhost:8765";

// Static build served by FastAPI (app/main.py) or Vercel. Risk numbers are precomputed from the
// Python engines into src/data/computed.json (uv run python -m scripts.build_consumer_data).
export default defineConfig({
  output: "static",
  vite: {
    plugins: [tailwindcss()],
    server: { proxy: { "/api": API, "/cds-services": API } },
  },
});
