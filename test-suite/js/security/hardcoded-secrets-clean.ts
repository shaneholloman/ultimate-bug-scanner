function requiredEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing ${name}`);
  }
  return value;
}

function loadRefreshToken(): string {
  return requiredEnv("REFRESH_TOKEN");
}

export const NEXTAUTH_SECRET = requiredEnv("NEXTAUTH_SECRET");

const stripeSecretKey = process.env.STRIPE_SECRET_KEY!;

export const mapsApiKey = requiredEnv("MAPS_API_KEY");

const authConfig = {
  jwtSecret: requiredEnv("JWT_SECRET"),
  clientSecret: requiredEnv("OAUTH_CLIENT_SECRET"),
  session: {
    secret: requiredEnv("SESSION_SECRET"),
  },
};

export const webhookConfig = {
  signingSecret: requiredEnv("STRIPE_WEBHOOK_SECRET"),
  refreshToken: loadRefreshToken(),
};

export const displayConfig = {
  themeVariant: process.env.THEME_VARIANT || "dark",
  publicBaseUrl: process.env.NEXT_PUBLIC_APP_URL || "https://example.com",
};

export { authConfig, stripeSecretKey };
