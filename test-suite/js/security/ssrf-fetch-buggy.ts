import http from "http";
import https from "https";
import axios from "axios";
import got from "got";

type ExpressRequest = {
  query: Record<string, string | undefined>;
  body: Record<string, string | undefined>;
  headers: Record<string, string | undefined>;
};

export async function proxyQueryUrl(req: ExpressRequest): Promise<Response> {
  const targetUrl = req.query.url;
  return fetch(targetUrl!, { signal: AbortSignal.timeout(5000) });
}

export function fetchPreview(request: Request): Promise<unknown> {
  const imageUrl = new URL(request.url).searchParams.get("image");
  return axios.get(imageUrl!);
}

export function postWebhook(req: ExpressRequest): Promise<unknown> {
  const callbackUrl = req.body.callbackUrl;
  return got(callbackUrl!);
}

export function streamHeaderTarget(req: ExpressRequest): http.ClientRequest {
  const remoteEndpoint = req.headers["x-forward-to"];
  return http.get(remoteEndpoint!);
}

export function nextRouteProxy(request: { nextUrl: { searchParams: URLSearchParams } }): Promise<Response> {
  return fetch(request.nextUrl.searchParams.get("target")!, {
    signal: AbortSignal.timeout(5000),
  });
}

export function rawHttpsProxy(req: ExpressRequest): https.ClientRequest {
  return https.request(req.query.callback!);
}
