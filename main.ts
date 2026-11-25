// news-front-page-1125 — a make.fun news-image-20261125 entry.
//
// The entry image (entry.png, beside this file) is a newspaper front page
// drawn programmatically for this competition: it sums up the world news of
// Wednesday 25 November 2026 in one 1024x1024 picture. The drawing code is
// generate_image.py; the PNG it produced is committed next to this program,
// and running this program publishes that exact PNG as the entry image.
//
// The grader runs the program with /output as the destination; locally,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
