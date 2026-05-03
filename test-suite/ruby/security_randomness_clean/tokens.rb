require "securerandom"

class SecureTokenFactory
  def reset_token
    "rst_#{SecureRandom.urlsafe_base64(32)}"
  end

  def session_secret
    SecureRandom.hex(32)
  end

  def csrf_nonce
    SecureRandom.uuid
  end

  def api_key
    "ak_#{SecureRandom.alphanumeric(40)}"
  end

  def display_theme
    ["light", "dark", "system"][rand(3)]
  end
end
