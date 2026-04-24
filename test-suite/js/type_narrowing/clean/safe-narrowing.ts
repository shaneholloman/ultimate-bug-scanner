import { notFound, redirect as nextRedirect } from "next/navigation";

interface Demo { value?: string; }
interface UserProfile { email?: string; }

function useDemo(x?: Demo) {
  if (!x?.value) {
    return "nope";
  }
  return x.value.toUpperCase();
}

// Multiline default params should not be misread as global assignments.
const addDefaults = (
  a = 1,
  b = 2,
): number => a + b;

addDefaults();

type Session = { user: { email: string } } | null;

export function requireSession(session: Session): string {
  if (!session) {
    nextRedirect("/login");
  }

  return session.user.email.toLowerCase();
}

export function requireProfile(profile?: UserProfile): string {
  if (!profile) {
    notFound();
  }

  return profile.email ?? "anonymous@example.com";
}
