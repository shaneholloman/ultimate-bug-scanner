class PredictableTokenFactory
  def reset_token
    token = rand(36**32).to_s(36)
    "rst_#{token}"
  end

  def session_secret
    secret = Random.rand(1_000_000_000).to_s
    "sess_#{secret}"
  end

  def csrf_nonce
    nonce = Time.now.to_i.to_s(36)
    "csrf_#{nonce}"
  end

  def api_key
    "ak_#{Process.pid}_#{object_id}"
  end

  def one_time_password
    rng = Random.new
    otp = rng.rand(1_000_000).to_s.rjust(6, "0")
    "otp_#{otp}"
  end
end
