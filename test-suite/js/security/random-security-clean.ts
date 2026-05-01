import { randomBytes, randomInt, randomUUID } from "crypto";

export function generatePasswordResetToken(): string {
  return randomBytes(32).toString("base64url");
}

export function createOtpCode(): string {
  return randomInt(0, 1_000_000).toString().padStart(6, "0");
}

export function createSessionId(userId: string): string {
  return `${userId}-${randomUUID()}`;
}

export function csrfNonce(): string {
  return randomBytes(16).toString("base64url");
}

export function animationJitter(): number {
  return Math.random() * 12;
}
