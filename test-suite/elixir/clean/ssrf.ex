defmodule CleanSsrf do
  @allowed_hosts MapSet.new(["api.example.com", "hooks.example.com"])

  def safe_outbound_url(raw) do
    uri = URI.parse(raw)

    unless uri.scheme == "https" and MapSet.member?(@allowed_hosts, uri.host) do
      raise ArgumentError, "blocked outbound URL"
    end

    raw
  end

  def fetch_req(conn) do
    target = safe_outbound_url(conn.params["url"] || "https://api.example.com/status")
    Req.get!(target)
  end

  def fetch_callback(conn) do
    callback =
      conn
      |> Plug.Conn.get_req_header("x-callback-url")
      |> List.first()
      |> safe_outbound_url()

    HTTPoison.get!(callback)
  end

  def fetch_with_finch(conn) do
    target = safe_outbound_url(conn.params["target"] || "https://api.example.com/status")

    Finch.build(:get, target)
    |> Finch.request(MyApp.Finch)
  end

  def fetch_with_tesla(params) do
    endpoint = safe_outbound_url(Map.get(params, "endpoint") || "https://hooks.example.com")
    Tesla.get(client(), endpoint)
  end

  def fetch_after_inline_validation(conn) do
    raw = conn.params["next_url"] || "https://api.example.com/status"
    uri = URI.parse(raw)

    unless uri.scheme == "https" and MapSet.member?(@allowed_hosts, uri.host) do
      raise ArgumentError, "blocked outbound URL"
    end

    Req.get!(raw)
  end

  defp client do
    Tesla.client([])
  end
end
