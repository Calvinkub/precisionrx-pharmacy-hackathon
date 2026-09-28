// @ts-check
import { defineConfig } from "astro/config";
import svelte from "@astrojs/svelte";

const API = "http://localhost:8765";

// Static build served by FastAPI (app/main.py). In dev, API calls are proxied to the Python server.
export default defineConfig({
  integrations: [svelte()],
  output: "static",
  vite: {
    server: {
      proxy: { "/api": API, "/cds-services": API },
    },
  },
});
