defmodule BuggyHeaderInjection do
  import Plug.Conn

  def display_name(conn) do
    name = conn.params["display_name"]

    conn
    |> put_resp_header("x-display-name", name)
    |> send_resp(200, "ok")
  end

  def download(conn) do
    filename = Map.get(conn.query_params, "filename")

    conn
    |> put_resp_header("content-disposition", "attachment; filename=\"#{filename}\"")
    |> send_resp(200, "ok")
  end

  def trace_header(conn) do
    trace =
      conn
      |> Plug.Conn.get_req_header("x-trace-id")
      |> List.first()

    Plug.Conn.put_resp_header(conn, "x-upstream-trace", trace)
  end

  def cookie_header(conn) do
    export_name = conn.cookies["export_name"]
    put_resp_header(conn, "x-export-name", export_name)
  end

  def content_type(conn) do
    media_type = conn.params["content_type"]
    put_resp_content_type(conn, media_type)
  end

  def mixed_location_and_display(conn) do
    tenant = conn.params["tenant"]
    put_resp_headers(conn, [{"location", "/safe"}, {"x-tenant", tenant}])
  end

  def validation_after_write(conn) do
    value = conn.params["customer"]
    response = put_resp_header(conn, "x-customer", value)

    if String.contains?(value, "\n") do
      raise ArgumentError, "invalid header"
    end

    response
  end
end
