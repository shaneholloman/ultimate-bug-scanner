require 'net/http'
require 'open-uri'
require 'faraday'
require 'httparty'
require 'rest-client'

class CallbackProxy
  ALLOWED_HOSTS = %w[api.example.com hooks.example.com].freeze

  def safe_outbound_url(raw)
    uri = URI.parse(raw)
    unless uri.scheme == 'https' && ALLOWED_HOSTS.include?(uri.host)
      raise ArgumentError, 'blocked outbound URL'
    end
    uri
  end

  def fetch_query
    target = safe_outbound_url(params[:url])
    Net::HTTP.get(target)
  end

  def fetch_callback
    callback = safe_outbound_url(request.headers['X-Callback-Url'])
    Faraday.get(callback)
  end

  def fetch_next
    next_url = safe_outbound_url(request.params.fetch(:next))
    URI.open(next_url)
  end

  def post_webhook
    webhook = safe_outbound_url(Rack::Request.new(env).params['webhook'])
    RestClient.post(webhook, '{}')
  end

  def fetch_host
    target = safe_outbound_url(params[:url])
    HTTParty.get(target)
  end

  def fetch_request_host
    target = safe_outbound_url("https://#{request.host}/status")
    Net::HTTP.get(target)
  end
end
