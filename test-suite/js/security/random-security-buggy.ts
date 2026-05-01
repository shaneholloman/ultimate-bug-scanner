export function generatePasswordResetToken(): string {
  return Math.random().toString(36).slice(2);
}

export function createOtpCode(): string {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

export function createSessionId(userId: string): string {
  const sid = `${userId}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return sid;
}

export function csrfNonce(): string {
  const nonce = Buffer.from(String(Math.random())).toString("base64url");
  return nonce;
}

export function makeInviteCode(): string {
  const inviteCode = Math.random().toString(36).slice(2, 10);
  return inviteCode;
}
