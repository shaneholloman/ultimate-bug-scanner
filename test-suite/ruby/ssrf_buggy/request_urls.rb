require 'net/http'
require 'open-uri'
require 'faraday'
require 'httparty'
require 'rest-client'

class CallbackProxy
  def fetch_query
    target = params[:url]
    Net::HTTP.get(URI.parse(target))
  end

  def fetch_callback
    callback = request.headers['X-Callback-Url']
    Faraday.get(callback)
  end

  def fetch_next
    next_url = request.params.fetch(:next)
    URI.open(next_url)
  end

  def post_webhook
    webhook = Rack::Request.new(env).params['webhook']
    RestClient.post(webhook, '{}')
  end

  def fetch_host
    host = params[:host]
    HTTParty.get("https://#{host}/internal/status")
  end

  def validate_too_late
    target = params[:late_url]
    Net::HTTP.get(URI.parse(target))
    raise ArgumentError unless URI.parse(target).host == 'api.example.com'
  end
end
