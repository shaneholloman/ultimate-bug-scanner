# frozen_string_literal: true

class RedirectController
  def query_redirect
    target = params[:return_url]
    redirect_to target
  end

  def header_redirect
    callback = request.headers["X-Return-To"]
    redirect callback
  end

  def rack_redirect(env)
    next_url = Rack::Request.new(env).params["next"]
    response["Location"] = next_url
  end

  def referer_redirect
    target = request.referer
    redirect_to(target)
  end

  def host_redirect
    destination = "https://#{request.host}/login"
    redirect_to destination
  end

  def late_validation
    target = params.fetch(:continue)
    redirect_to target
    raise ArgumentError unless URI.parse(target).host == "app.example.com"
  end
end
