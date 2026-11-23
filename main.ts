// news-image-20261122 entry (Node 22, standard library only).
// The image this entry submits is entry.png, rendered by generate.py
// (Pillow) from the researched news of Sunday 22 November 2026 and held
// in this repository. This program copies it to the grader's output
// directory as entry.png. The copy is byte-for-byte deterministic:
// running it twice writes the same bytes both times.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
