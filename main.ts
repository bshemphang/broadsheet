// Broadsheet: one image summing up the world's news of Saturday 21 November 2026.
// The image is drawn by tools/draw.py and shipped as entry.png; this program
// copies it to the grader's output directory, unchanged, every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
