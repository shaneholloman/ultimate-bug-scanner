# frozen_string_literal: true

require "uri"

class RedirectController
  ALLOWED_REDIRECT_HOSTS = %w[app.example.com accounts.example.com].freeze

  def safe_redirect_url(raw)
    return raw if raw.to_s.start_with?("/") && !raw.to_s.start_with?("//")

    uri = URI.parse(raw.to_s)
    unless uri.scheme == "https" && ALLOWED_REDIRECT_HOSTS.include?(uri.host)
      raise ArgumentError, "blocked redirect"
    end

    uri.to_s
  end

  def query_redirect
    target = safe_redirect_url(params[:return_url])
    redirect_to target
  end

  def header_redirect
    callback = safe_redirect_url(request.headers["X-Return-To"])
    redirect callback
  end

  def rack_redirect(env)
    next_url = safe_redirect_url(Rack::Request.new(env).params["next"])
    response["Location"] = next_url
  end

  def local_guard_redirect
    target = params.fetch(:continue)
    unless target.start_with?("/") && !target.start_with?("//")
      head :bad_request
      return
    end

    redirect_to target
  end

  def rails_url_from_redirect
    target = url_from(params[:return_url]) || root_path
    redirect_to target, allow_other_host: false
  end
end
