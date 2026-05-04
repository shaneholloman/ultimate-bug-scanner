defmodule BuggyHardcodedSecrets do
  @api_key "sk_live_1234567890abcdef"

  def endpoint_config do
    [
      secret_key_base: "2f4a8b9c0d1e2f3a4b5c6d7e8f901234",
      live_view: [
        signing_salt: "hardcoded_live_view_salt"
      ]
    ]
  end

  def guardian_config do
    [
      issuer: "example",
      secret_key: "guardian_jwt_secret_1234567890",
      jwt_secret: System.get_env("JWT_SECRET", "fallback_jwt_secret_123456")
    ]
  end

  def webhook_config do
    %{
      client_secret: "stripe_webhook_secret_1234567890",
      refresh_token: "refresh_token_from_dashboard_12345"
    }
  end
end
