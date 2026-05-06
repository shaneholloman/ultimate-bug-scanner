const MAX_BODY_BYTES = 1024 * 1024;

type ImportResult = {
  accepted: number;
};

export async function POST(request: Request): Promise<Response> {
  const contentLength = Number(request.headers.get("content-length") ?? "0");
  if (!Number.isFinite(contentLength) || contentLength > MAX_BODY_BYTES) {
    return Response.json({ error: "payload too large" }, { status: 413 });
  }

  const payload = await request.json();
  return Response.json({ accepted: payload.items.length } satisfies ImportResult);
}

export async function PUT(req: Request): Promise<Response> {
  const contentLength = Number(req.headers.get("content-length") ?? "0");
  if (contentLength > MAX_BODY_BYTES) {
    return new Response("payload too large", { status: 413 });
  }

  const rawCsv = await req.text();
  return new Response(rawCsv.slice(0, 32));
}
