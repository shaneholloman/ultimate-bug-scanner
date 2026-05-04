defmodule CleanHardcodedSecrets do
  def endpoint_config do
    [
      secret_key_base: System.fetch_env!("SECRET_KEY_BASE"),
      live_view: [
        signing_salt: System.fetch_env!("LIVE_VIEW_SIGNING_SALT")
      ]
    ]
  end

  def guardian_config do
    [
      issuer: "example",
      secret_key: {:system, "GUARDIAN_SECRET_KEY"},
      jwt_secret: System.fetch_env!("JWT_SECRET")
    ]
  end

  def webhook_config do
    %{
      client_secret: System.fetch_env!("STRIPE_WEBHOOK_SECRET"),
      refresh_token: load_refresh_token()
    }
  end

  def display_config do
    [
      theme_token: System.get_env("THEME_VARIANT", "dark")
    ]
  end

  defp load_refresh_token do
    System.fetch_env!("REFRESH_TOKEN")
  end
end
