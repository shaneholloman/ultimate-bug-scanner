type RequestLike = {
  query: Record<string, string | undefined>;
  body: Record<string, string | undefined>;
  headers: Record<string, string | undefined>;
  nextUrl: { searchParams: URLSearchParams };
};

type ResponseLike = {
  setHeader(name: string, value: string): void;
  header(name: string, value: string): void;
};

function sanitizeHeaderValue(value: string | null | undefined): string {
  const clean = String(value ?? "").replace(/[\r\n]/g, "");
  if (clean.length === 0) {
    throw new Error("empty header value");
  }
  return clean;
}

function encodeFilename(filename: string | undefined): string {
  return encodeURIComponent(filename ?? "report.pdf");
}

export function expressHeader(req: RequestLike, res: ResponseLike): void {
  res.setHeader("X-Display-Name", sanitizeHeaderValue(req.query.name));
}

export function contentDisposition(req: RequestLike, res: ResponseLike): void {
  const filename = encodeFilename(req.query.filename);
  res.setHeader("Content-Disposition", `attachment; filename*=UTF-8''${filename}`);
}

export function fastifyReply(req: RequestLike, reply: ResponseLike): void {
  reply.header("X-Trace", sanitizeHeaderValue(req.headers["x-trace-id"]));
}

export function responseObject(request: RequestLike): Response {
  const token = request.nextUrl.searchParams.get("token");
  return new Response("ok", {
    headers: {
      "X-Token": sanitizeHeaderValue(token),
    },
  });
}

export function headersApi(req: RequestLike): Headers {
  const responseHeaders = new Headers();
  responseHeaders.set("X-Session", sanitizeHeaderValue(req.body.session));
  return responseHeaders;
}
