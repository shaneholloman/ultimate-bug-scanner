type RequestLike = {
  query: Record<string, string | undefined>;
  body: Record<string, string | undefined>;
  headers: Record<string, string | undefined>;
  nextUrl: { searchParams: URLSearchParams };
};

type ResponseLike = {
  setHeader(name: string, value: string | undefined): void;
  header(name: string, value: string | undefined): void;
};

export function expressHeader(req: RequestLike, res: ResponseLike): void {
  res.setHeader("X-Display-Name", req.query.name);
}

export function contentDisposition(req: RequestLike, res: ResponseLike): void {
  const filename = req.query.filename;
  const attachmentHeader = `attachment; filename="${filename}"`;
  res.setHeader("Content-Disposition", attachmentHeader);
}

export function fastifyReply(req: RequestLike, reply: ResponseLike): void {
  const traceId = req.headers["x-trace-id"];
  reply.header("X-Trace", traceId);
}

export function responseObject(request: RequestLike): Response {
  const token = request.nextUrl.searchParams.get("token");
  return new Response("ok", {
    headers: {
      "X-Token": token ?? "",
    },
  });
}

export function headersApi(req: RequestLike): Headers {
  const responseHeaders = new Headers();
  responseHeaders.set("X-Session", req.body.session ?? "");
  return responseHeaders;
}
