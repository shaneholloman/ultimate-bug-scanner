defmodule BuggyOpenRedirect do
  import Phoenix.Controller
  import Plug.Conn

  def redirect_query(conn) do
    target = conn.params["next"]
    redirect(conn, to: target)
  end

  def redirect_header(conn) do
    target =
      conn
      |> Plug.Conn.get_req_header("x-redirect-url")
      |> List.first()

    Phoenix.Controller.redirect(conn, external: target)
  end

  def redirect_query_params(conn) do
    callback = Map.get(conn.query_params, "return_to")
    redirect(conn, external: callback)
  end

  def redirect_host(conn) do
    target = "https://" <> conn.host <> "/dashboard"
    redirect(conn, external: target)
  end

  def redirect_location_header(conn) do
    location = conn.params["location"]

    conn
    |> put_resp_header("location", location)
    |> send_resp(302, "")
  end

  def validate_after_redirect(conn) do
    target = conn.params["continue"]
    response = redirect(conn, to: target)

    unless String.starts_with?(target, "/") and not String.starts_with?(target, "//") do
      raise ArgumentError, "blocked redirect"
    end

    response
  end
end
