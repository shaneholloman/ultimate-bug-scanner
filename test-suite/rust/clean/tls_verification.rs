use native_tls::TlsConnector;
use openssl::ssl::{SslConnector, SslMethod, SslVerifyMode};
use reqwest::{Certificate, ClientBuilder};

const ACCEPT_INVALID_CERTS: bool = false;

fn reqwest_uses_default_tls() -> reqwest::Result<reqwest::Client> {
    ClientBuilder::new().https_only(true).build()
}

fn reqwest_uses_private_root(ca: Certificate) -> reqwest::Result<reqwest::Client> {
    ClientBuilder::new()
        .add_root_certificate(ca)
        .danger_accept_invalid_certs(false)
        .danger_accept_invalid_hostnames(false)
        .build()
}

fn reqwest_uses_private_root_with_safe_constant(
    ca: Certificate,
) -> reqwest::Result<reqwest::Client> {
    ClientBuilder::new()
        .add_root_certificate(ca)
        .danger_accept_invalid_certs(ACCEPT_INVALID_CERTS)
        .build()
}

fn reqwest_keeps_hostname_verification_from_local() -> reqwest::Result<reqwest::Client> {
    let accept_invalid_hostnames = false;
    ClientBuilder::new()
        .danger_accept_invalid_hostnames(accept_invalid_hostnames)
        .build()
}

fn native_tls_keeps_verification() -> Result<TlsConnector, native_tls::Error> {
    TlsConnector::builder().build()
}

fn openssl_keeps_peer_verification() -> Result<SslConnector, openssl::error::ErrorStack> {
    let mut builder = SslConnector::builder(SslMethod::tls())?;
    builder.set_verify(SslVerifyMode::PEER);
    Ok(builder.build())
}
