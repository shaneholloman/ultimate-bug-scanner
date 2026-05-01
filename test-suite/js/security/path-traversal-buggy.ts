import fs from "node:fs";
import path from "node:path";

type RequestLike = {
  query: Record<string, string | undefined>;
  params: Record<string, string | undefined>;
  body: Record<string, string | undefined>;
  get(name: string): string | undefined;
  header(name: string): string | undefined;
  file?: UploadedFile;
  files?: Record<string, UploadedFile | undefined>;
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

const UPLOAD_ROOT = "/srv/app/uploads";

export function expressDownload(req: RequestLike, res: ResponseLike): void {
  const requested = req.query.file;
  res.sendFile(path.join(UPLOAD_ROOT, requested ?? ""));
}

export function rawRead(req: RequestLike): Buffer {
  const filePath = req.params.name;
  return fs.readFileSync(path.resolve(UPLOAD_ROOT, filePath ?? ""));
}

export async function uploadedFileSave(req: RequestLike): Promise<void> {
  const uploaded = req.file;
  if (!uploaded) {
    throw new Error("missing upload");
  }
  const target = path.join(UPLOAD_ROOT, uploaded.originalname);
  await uploaded.mv(target);
}

export function bodyPathWrite(req: RequestLike): void {
  const output = path.join(UPLOAD_ROOT, req.body.destination ?? "report.txt");
  fs.writeFileSync(output, "generated report");
}

export function directDownload(req: RequestLike, res: ResponseLike): void {
  res.download(path.join(UPLOAD_ROOT, req.query.archive ?? ""));
}

export function headerPathRead(req: RequestLike): Buffer {
  const requested = req.get("x-file-path");
  return fs.readFileSync(path.join(UPLOAD_ROOT, requested ?? ""));
}

export function headerPathWrite(req: RequestLike): void {
  const destination = req.header("x-output-path");
  fs.writeFileSync(path.join(UPLOAD_ROOT, destination ?? "report.txt"), "generated report");
}

export async function nextHeaderPathRead(): Promise<Buffer> {
  const incomingHeaders = await headers();
  const requested = incomingHeaders.get("x-file-path");
  return fs.readFileSync(path.join(UPLOAD_ROOT, requested ?? ""));
}
