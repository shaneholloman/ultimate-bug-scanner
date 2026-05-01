defmodule BuggySsrf do
  def fetch_req(conn) do
    target = conn.params["url"]
    Req.get!(target)
  end

  def fetch_callback(conn) do
    callback = Plug.Conn.get_req_header(conn, "x-callback-url") |> List.first()
    HTTPoison.get!(callback)
  end

  def fetch_with_finch(conn) do
    host = conn.host
    url = "https://" <> host <> "/internal/status"

    Finch.build(:get, url)
    |> Finch.request(MyApp.Finch)
  end

  def fetch_with_tesla(params) do
    endpoint = Map.get(params, "endpoint")
    Tesla.get(client(), endpoint)
  end

  def fetch_with_httpc(conn) do
    target = conn.query_params["target"]
    :httpc.request(:get, {String.to_charlist(target), []}, [], [])
  end

  def validate_too_late(conn) do
    target = conn.params["callback_url"]
    response = Req.get!(target)
    uri = URI.parse(target)

    unless uri.scheme == "https" and uri.host == "api.example.com" do
      raise ArgumentError, "blocked outbound URL"
    end

    response
  end

  defp client do
    Tesla.client([])
  end
end
