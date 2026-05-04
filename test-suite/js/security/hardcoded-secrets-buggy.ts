export const NEXTAUTH_SECRET = "nextauth_secret_1234567890abcdef";

const stripeSecretKey = "sk_live_1234567890abcdef";

const authConfig = {
  jwtSecret: "jwt_secret_from_dashboard_123456",
  clientSecret: "oauth_client_secret_1234567890",
  session: {
    secret: "session_cookie_secret_123456",
  },
};

export function getJwtSecret(): string {
  return process.env.JWT_SECRET || "fallback_jwt_secret_123456";
}

export const webhookConfig = {
  signingSecret: process.env.STRIPE_WEBHOOK_SECRET ?? "whsec_fallback_1234567890",
  refreshToken: "refresh_token_from_console_123456",
};

export const mapsApiKey = process.env.MAPS_API_KEY || "maps_api_key_1234567890abcdef";

export function makeAuthHeader(): string {
  const bearerToken = "bearer_token_from_admin_console_123456";
  return `Bearer ${bearerToken}`;
}

export { authConfig, stripeSecretKey };
