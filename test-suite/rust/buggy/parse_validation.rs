use std::convert::TryInto;
use std::env;

fn parse_inferred(raw: &str) -> u16 {
    raw.parse().unwrap()
}

fn parse_typed(raw: &str) -> usize {
    raw.parse::<usize>().expect("count should parse")
}

fn parse_json(raw: &str) -> serde_json::Value {
    serde_json::from_str(raw).unwrap()
}

fn parse_json_slice(raw: &[u8]) -> serde_json::Value {
    serde_json::from_slice(raw).expect("valid json bytes")
}

fn parse_toml(raw: &str) -> toml::Value {
    toml::from_str(raw).unwrap()
}

fn read_mode() -> String {
    env::var("APP_MODE").unwrap()
}

fn read_path() -> std::ffi::OsString {
    std::env::var_os("PATH").expect("PATH should exist")
}

fn narrow_port(raw: u64) -> u16 {
    raw.try_into().unwrap()
}
