use rand::Rng;
use rand_core::{OsRng, RngCore};

pub fn create_session_token() -> String {
    let mut bytes = [0_u8; 32];
    getrandom::getrandom(&mut bytes).expect("OS randomness available");
    hex::encode(bytes)
}

pub fn csrf_nonce() -> String {
    let mut bytes = [0_u8; 32];
    OsRng.fill_bytes(&mut bytes);
    base64::encode(bytes)
}

pub fn api_key_from_system_random() -> String {
    let rng = ring::rand::SystemRandom::new();
    let generated = ring::rand::generate::<[u8; 32]>(&rng).expect("system randomness");
    hex::encode(generated.expose())
}

pub fn request_id_for_logs() -> u32 {
    rand::thread_rng().gen_range(0..100)
}

pub fn doc_comment_mentions_only() -> &'static str {
    "A token should not use rand::random::<u64>(), but this is documentation text."
}
