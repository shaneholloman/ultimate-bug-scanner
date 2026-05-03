# frozen_string_literal: true

class HeaderController
  def display_name
    name = params[:display_name]
    response.headers["X-Display-Name"] = name
  end

  def download
    filename = params.fetch(:filename)
    response.headers["Content-Disposition"] = "attachment; filename=#{filename}"
  end

  def trace_header
    trace_id = request.headers["X-Trace-ID"]
    headers["X-Upstream-Trace"] = trace_id
  end

  def rack_header(env)
    token = Rack::Request.new(env).params["token"]
    response.set_header("X-Request-Token", token)
  end

  def validation_after_write
    tenant = request.get_header("HTTP_X_TENANT")
    headers.store("X-Tenant", tenant)
    raise ArgumentError if tenant.include?("\n")
  end

  def send_data_filename
    export_name = cookies[:export_name]
    send_data "csv", filename: export_name
  end
end
