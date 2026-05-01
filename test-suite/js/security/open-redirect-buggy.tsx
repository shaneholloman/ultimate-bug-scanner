import { redirect, useRouter, useSearchParams } from "next/navigation";

type HeaderRequest = {
  headers: Record<string, string | undefined>;
  get(name: string): string | undefined;
};

export function LoginRedirectButton() {
  const router = useRouter();
  const searchParams = useSearchParams();

  function handleLoginSuccess(): void {
    const returnTo = searchParams.get("returnTo") || "/";
    router.push(returnTo);
  }

  return <button onClick={handleLoginSuccess}>Continue</button>;
}

export function redirectReferer(req: HeaderRequest): never {
  const returnTo = req.headers.referer || "/";
  redirect(returnTo);
}

export function redirectHeaderMethod(req: HeaderRequest): never {
  const nextUrl = req.get("x-next-url") || "/";
  redirect(nextUrl);
}
