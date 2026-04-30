type ApiUser = {
  id: string;
  email: string;
};

export async function loadUser(userId: string, signal: AbortSignal): Promise<ApiUser> {
  const response = await fetch(`/api/users/${encodeURIComponent(userId)}`, { signal });
  return response.json() as Promise<ApiUser>;
}

export function saveUser(user: ApiUser): Promise<Response> {
  return fetch("/api/users", {
    method: "POST",
    signal: AbortSignal.timeout(5000),
    headers: { "content-type": "application/json" },
    body: JSON.stringify(user),
  });
}

export function loadAuditTrail(userId: string): Promise<Response> {
  const requestInit: RequestInit = {
    signal: AbortSignal.timeout(3000),
  };

  return window.fetch(`/api/users/${encodeURIComponent(userId)}/audit`, requestInit);
}
