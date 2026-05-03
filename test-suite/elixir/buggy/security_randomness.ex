defmodule BuggySecurityRandomness do
  def reset_token do
    token =
      :rand.bytes(32)
      |> Base.url_encode64(padding: false)

    {:ok, token}
  end

  def session_secret(conn) do
    secret = Integer.to_string(:rand.uniform(1_000_000_000))
    Plug.Conn.put_session(conn, :session_secret, secret)
  end

  def csrf_nonce(conn) do
    nonce = Enum.random(100_000..999_999)
    Plug.Conn.put_resp_cookie(conn, "_csrf", Integer.to_string(nonce))
  end

  def api_key do
    "ak_" <> Integer.to_string(System.unique_integer([:positive]))
  end

  def random_token do
    :rand.uniform(9_999_999)
  end
end
