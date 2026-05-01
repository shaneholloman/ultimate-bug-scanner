package security

import (
	"errors"
	"net/http"
	"net/url"
)

var allowedHosts = map[string]bool{
	"api.example.com":   true,
	"hooks.example.com": true,
}

func safeOutboundURL(raw string) (string, error) {
	parsed, err := url.Parse(raw)
	if err != nil {
		return "", err
	}
	if parsed.Scheme != "https" || !allowedHosts[parsed.Hostname()] {
		return "", errors.New("blocked outbound host")
	}
	return parsed.String(), nil
}

func proxyAllowedURL(r *http.Request) (*http.Response, error) {
	target, err := safeOutboundURL(r.URL.Query().Get("url"))
	if err != nil {
		return nil, err
	}
	return http.Get(target)
}

func postAllowedCallback(r *http.Request) (*http.Response, error) {
	target, err := safeOutboundURL(r.FormValue("callback"))
	if err != nil {
		return nil, err
	}
	return http.Post(target, "application/json", nil)
}

func fetchAllowedRequest(r *http.Request, client *http.Client) (*http.Response, error) {
	target, err := safeOutboundURL(r.Header.Get("X-Webhook-Url"))
	if err != nil {
		return nil, err
	}
	req, err := http.NewRequestWithContext(r.Context(), http.MethodGet, target, nil)
	if err != nil {
		return nil, err
	}
	return client.Do(req)
}
