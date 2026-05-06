type ImportResult = {
  accepted: number;
};

export async function POST(request: Request): Promise<Response> {
  const payload = await request.json();
  return Response.json({ accepted: payload.items.length } satisfies ImportResult);
}

export async function PUT(req: Request): Promise<Response> {
  const rawCsv = await req.text();
  return new Response(rawCsv.slice(0, 32));
}

export async function handleUpload(event: { request: Request }): Promise<Response> {
  const form = await event.request.formData();
  return Response.json({ files: form.getAll("file").length });
}
