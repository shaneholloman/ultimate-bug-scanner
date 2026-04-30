import fs from "node:fs";
import path from "node:path";

type ZipEntry = {
  path: string;
  stream(): NodeJS.ReadableStream;
};

type TarHeader = {
  name: string;
};

function safeArchiveTarget(destination: string, entryName: string): string {
  const base = path.resolve(destination);
  const target = path.resolve(base, entryName);
  const relative = path.relative(base, target);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error("archive entry escaped extraction directory");
  }
  return target;
}

export function extractZipEntry(entry: ZipEntry, destination: string): void {
  const outputPath = safeArchiveTarget(destination, entry.path);
  entry.stream().pipe(fs.createWriteStream(outputPath));
}

export function extractTarHeader(header: TarHeader, destination: string, contents: Buffer): void {
  const outputPath = safeArchiveTarget(destination, path.basename(header.name));
  fs.writeFileSync(outputPath, contents);
}
