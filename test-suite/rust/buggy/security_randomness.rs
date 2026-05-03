use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::time::{SystemTime, UNIX_EPOCH};

pub fn create_session_token() -> String {
    let mut rng = rand::thread_rng();
    format!("sess-{:x}", rng.gen::<u128>())
}

pub fn csrf_nonce() -> String {
    rand::random::<u64>().to_string()
}

pub fn invite_code() -> String {
    fastrand::u64(..).to_string()
}

pub fn api_key_from_seed(user_id: &str) -> String {
    let seed = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos() as u64;
    let mut rng = StdRng::seed_from_u64(seed);
    format!("ak_{user_id}_{:x}", rng.gen::<u64>())
}

pub fn password_reset_token(email: &str) -> String {
    let mut hasher = DefaultHasher::new();
    email.hash(&mut hasher);
    format!("reset-{:x}", hasher.finish())
}

pub fn otp_code() -> String {
    format!("{:06}", std::process::id() % 1_000_000)
}

pub fn display_jitter_bucket() -> u32 {
    rand::thread_rng().gen_range(0..100)
}
