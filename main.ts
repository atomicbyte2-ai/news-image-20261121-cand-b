// news-image-20261121-cand-b: runs build_entry.py (Python + PIL) which
// generates entry.png deterministically from the verified 35-story list
// for Saturday 21 November 2026, then writes it to the output dir.
// All paths resolve from this file's own directory; no relative paths,
// no network. Output defaults to /output (or MAKEFUN_OUTPUT_DIR).
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const here = fileURLToPath(new URL(".", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });

execFileSync("python3", [join(here, "build_entry.py"), outDir], {
  stdio: "inherit",
});

const outPath = join(outDir, "entry.png");
const size = statSync(outPath).size;
if (size === 0) {
  throw new Error(`entry.png is empty (0 bytes) at ${outPath}`);
}
if (size > 1048576) {
  throw new Error(
    `entry.png too large: ${size} bytes exceeds 1 MiB limit (1048576 bytes)`,
  );
}
const bytes = readFileSync(outPath);
if (bytes.subarray(1, 4).toString("ascii") !== "PNG") {
  throw new Error(`entry.png at ${outPath} is not a PNG file`);
}
console.log(`entry.png written to ${outPath} (${size} bytes)`);
