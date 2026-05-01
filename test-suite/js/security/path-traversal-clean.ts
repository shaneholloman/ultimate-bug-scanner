import fs from "node:fs";
import path from "node:path";

type RequestLike = {
  query: Record<string, string | undefined>;
  params: Record<string, string | undefined>;
  body: Record<string, string | undefined>;
  get(name: string): string | undefined;
  header(name: string): string | undefined;
  file?: UploadedFile;
};

type ResponseLike = {
  sendFile(filePath: string): void;
  download(filePath: string): void;
};

type UploadedFile = {
  name: string;
  originalname: string;
  mv(destination: string): Promise<void>;
};

type HeaderBag = {
  get(name: string): string | null;
};

declare function headers(): Promise<HeaderBag>;

const UPLOAD_ROOT = path.resolve("/srv/app/uploads");

function validatePath(rawName: string | undefined): string {
  if (!rawName) {
    throw new Error("missing file name");
  }
  const target = path.resolve(UPLOAD_ROOT, rawName);
  const relative = path.relative(UPLOAD_ROOT, target);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error("path escaped upload root");
  }
  return target;
}

function sanitizeFilename(rawName: string | undefined): string {
  return path.basename(rawName ?? "upload.bin");
}

export function expressDownload(req: RequestLike, res: ResponseLike): void {
  const requested = req.query.file;
  res.sendFile(validatePath(requested));
}

export function rawRead(req: RequestLike): Buffer {
  const filePath = validatePath(req.params.name);
  return fs.readFileSync(filePath);
}

export async function uploadedFileSave(req: RequestLike): Promise<void> {
  const uploaded = req.file;
  if (!uploaded) {
    throw new Error("missing upload");
  }
  const target = path.join(UPLOAD_ROOT, sanitizeFilename(uploaded.originalname));
  await uploaded.mv(target);
}

export function bodyPathWrite(req: RequestLike): void {
  const output = validatePath(req.body.destination);
  fs.writeFileSync(output, "generated report");
}

export function directDownload(req: RequestLike, res: ResponseLike): void {
  res.download(validatePath(req.query.archive));
}

export function headerPathRead(req: RequestLike): Buffer {
  const requested = req.get("x-file-path");
  return fs.readFileSync(validatePath(requested));
}

export function headerPathWrite(req: RequestLike): void {
  const destination = validatePath(req.header("x-output-path"));
  fs.writeFileSync(destination, "generated report");
}

export async function nextHeaderPathRead(): Promise<Buffer> {
  const incomingHeaders = await headers();
  const requested = incomingHeaders.get("x-file-path");
  return fs.readFileSync(validatePath(requested ?? undefined));
}
