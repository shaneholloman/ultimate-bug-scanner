defmodule CleanSecurityRandomness do
  def reset_token do
    token =
      :crypto.strong_rand_bytes(32)
      |> Base.url_encode64(padding: false)

    {:ok, token}
  end

  def session_secret(conn) do
    secret =
      :crypto.strong_rand_bytes(24)
      |> Base.encode64(padding: false)

    Plug.Conn.put_session(conn, :session_secret, secret)
  end

  def csrf_nonce(conn) do
    nonce = secure_token()
    Plug.Conn.put_resp_cookie(conn, "_csrf", nonce)
  end

  def random_theme do
    Enum.random(["light", "dark", "system"])
  end

  defp secure_token do
    :crypto.strong_rand_bytes(16)
    |> Base.url_encode64(padding: false)
  end
end
