// news-image-20261125 entry (Node 22, standard library only).
// The image is entry.png beside this file: a 1024x1024 infographic drawn by
// render.py from the verified news of Wednesday 25 November 2026.
// This program copies it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
// Outside the grader's container:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync, chmodSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const src = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

const buf = readFileSync(src);
if (buf.length < 8 || buf.readUInt32BE(0) !== 0x89504e47 || buf.readUInt32BE(4) !== 0x0d0a1a0a) {
  throw new Error('entry.png is not a PNG file');
}
if (buf.length > 1048576) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB gate`);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 gate`);
}
// A whole PNG ends with the IEND chunk (length 0, "IEND", CRC AE426082).
const iend = Buffer.from([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82]);
if (buf.length < 12 || !buf.subarray(buf.length - 12).equals(iend)) {
  throw new Error('entry.png does not end with a complete IEND chunk');
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
chmodSync(dest, 0o644);
// Read the copy back: a partial copy must fail here, not in the grader.
const back = readFileSync(dest);
if (back.length !== buf.length || !back.equals(buf)) {
  throw new Error(`copied ${dest} is ${back.length} bytes, source is ${buf.length}`);
}
console.log(`wrote ${dest} (${width}x${height}, ${statSync(dest).size} bytes)`);
