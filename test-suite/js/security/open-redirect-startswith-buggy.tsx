import { useRouter, useSearchParams } from "next/navigation";

export function LoginRedirectButton() {
  const router = useRouter();
  const searchParams = useSearchParams();

  function handleLoginSuccess(): void {
    const returnTo = searchParams.get("returnTo") || "/"; // TODO: add sameOrigin validation
    if (returnTo.startsWith("/")) {
      router.push(returnTo);
    }
  }

  return <button onClick={handleLoginSuccess}>Continue</button>;
}
