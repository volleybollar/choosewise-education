#!/usr/bin/env node
/*
  Image optimization pipeline for NotebookLM reference images.

  Input:  ~/Desktop/nlm-images-original/  (PNG/JPEG, any size, ~900 MB)
  Output: ../assets/notebooklm-images/
          style-NNN-400w.webp   (400px wide, quality 85)
          style-NNN-800w.webp   (800px wide, quality 85)
          style-NNN.webp        (1200px wide, quality 85)  ← default/fallback

  Images are sorted alphabetically so they are numbered by filename order.
  Produces ~80–120 MB total for 140 images (from ~900 MB source).

  Usage: node scripts/optimize-images.js
*/

import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const INPUT_DIR  = path.join(process.env.HOME, 'Desktop', 'nlm-images-original');
const OUTPUT_DIR = path.join(process.cwd(), '..', 'assets', 'notebooklm-images');
const WIDTHS  = [400, 800, 1200];
const QUALITY = 85;

async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  const allFiles = await fs.readdir(INPUT_DIR);
  const files = allFiles
    .filter(f => /\.(png|jpe?g|webp)$/i.test(f))
    // Sort numerically by the leading integer in the filename (1.png, 2.png, ..., 140.png).
    // Alphabetical sort would give 1, 10, 100, 101, ..., 2, 20, ... which breaks the
    // prompt→image pairing (prompts are indexed numerically in the source data).
    .sort((a, b) => {
      const na = parseInt(a.match(/^\d+/)?.[0] ?? '0', 10);
      const nb = parseInt(b.match(/^\d+/)?.[0] ?? '0', 10);
      return na - nb;
    });

  console.log(`Found ${files.length} source images in ${INPUT_DIR}`);
  console.log(`Output dir: ${OUTPUT_DIR}`);

  let totalBytesOut = 0;
  const startTime = Date.now();

  for (let i = 0; i < files.length; i++) {
    const src = path.join(INPUT_DIR, files[i]);
    const index = String(i + 1).padStart(3, '0');
    const baseName = `style-${index}`;

    for (const width of WIDTHS) {
      const outName = width === 1200
        ? `${baseName}.webp`
        : `${baseName}-${width}w.webp`;
      const outPath = path.join(OUTPUT_DIR, outName);

      const info = await sharp(src, { failOn: 'none' })
        .rotate()                          // auto-rotate based on EXIF
        .resize({ width, withoutEnlargement: true })
        .webp({ quality: QUALITY })
        .toFile(outPath);

      totalBytesOut += info.size;
    }

    if ((i + 1) % 20 === 0 || i === files.length - 1) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);
      console.log(`  ${i + 1}/${files.length} processed (${elapsed}s elapsed)`);
    }
  }

  const elapsedTotal = ((Date.now() - startTime) / 1000).toFixed(0);
  console.log(`\nDone.`);
  console.log(`Total output: ${(totalBytesOut / 1024 / 1024).toFixed(1)} MB`);
  console.log(`Total time:   ${elapsedTotal} seconds`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
