import { redirect, useRouter, useSearchParams } from "next/navigation";

type HeaderRequest = {
  headers: Record<string, string | undefined>;
  get(name: string): string | undefined;
};

function isSafeRedirectPath(value: string): boolean {
  return value.startsWith("/") && !value.startsWith("//");
}

export function LoginRedirectButton() {
  const router = useRouter();
  const searchParams = useSearchParams();

  function handleLoginSuccess(): void {
    const returnTo = searchParams.get("returnTo") || "/";
    if (isSafeRedirectPath(returnTo)) {
      router.push(returnTo);
      return;
    }
    router.push("/");
  }

  return <button onClick={handleLoginSuccess}>Continue</button>;
}

export function redirectSafeReferer(req: HeaderRequest): never {
  const returnTo = req.headers.referer || "/";
  if (isSafeRedirectPath(returnTo)) {
    redirect(returnTo);
  }
  redirect("/");
}

export function redirectSafeHeaderMethod(req: HeaderRequest): never {
  const nextUrl = req.get("x-next-url") || "/";
  if (isSafeRedirectPath(nextUrl)) {
    redirect(nextUrl);
  }
  redirect("/");
}
