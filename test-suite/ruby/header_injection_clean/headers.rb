# frozen_string_literal: true

require "cgi"
require "erb"

class HeaderController
  def safe_header_value(raw)
    raw.to_s.delete("\r\n")
  end

  def reject_crlf!(raw)
    if raw.to_s.match?(/[\r\n]/)
      head :bad_request
      return nil
    end

    raw.to_s
  end

  def display_name
    name = safe_header_value(params[:display_name])
    response.headers["X-Display-Name"] = name
  end

  def download
    filename = ERB::Util.url_encode(params.fetch(:filename).to_s)
    response.headers["Content-Disposition"] = "attachment; filename=#{filename}"
  end

  def trace_header
    trace_id = request.headers["X-Trace-ID"].to_s.gsub(/[\r\n]/, "")
    headers["X-Upstream-Trace"] = trace_id
  end

  def rack_header(env)
    token = Rack::Request.new(env).params["token"]
    clean_token = token.tr("\r\n", "")
    response.set_header("X-Request-Token", clean_token)
  end

  def guarded_header
    tenant = request.get_header("HTTP_X_TENANT")
    if tenant.include?("\r") || tenant.include?("\n")
      raise ArgumentError, "invalid header value"
    end

    headers.store("X-Tenant", tenant)
  end

  def send_data_filename
    export_name = CGI.escape(cookies[:export_name].to_s)
    send_data "csv", filename: export_name
  end

  def location_is_open_redirect_coverage
    target = url_from(params[:return_url]) || "/"
    response.headers["Location"] = target
  end
end
