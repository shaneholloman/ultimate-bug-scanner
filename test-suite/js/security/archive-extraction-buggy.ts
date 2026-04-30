import fs from "node:fs";
import path from "node:path";

type ZipEntry = {
  path: string;
  entryName: string;
  stream(): NodeJS.ReadableStream;
  getData(): Buffer;
};

type TarHeader = {
  name: string;
};

export function extractZipEntry(entry: ZipEntry, destination: string): void {
  const outputPath = path.join(destination, entry.path);
  entry.stream().pipe(fs.createWriteStream(outputPath));
}

export function extractAdmZipEntry(file: ZipEntry, destination: string): void {
  const archiveName = file.entryName;
  fs.writeFileSync(path.resolve(destination, archiveName), file.getData());
}

export function extractTarHeader(header: TarHeader, destination: string, contents: Buffer): void {
  const outputPath = path.join(destination, header.name);
  fs.writeFileSync(outputPath, contents);
}
