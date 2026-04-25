fn documentation_mentions_only() -> &'static str {
    r#"
    Examples in prose should not trigger parser robustness warnings:
    raw.parse::<usize>().unwrap()
    serde_json::from_str(raw).unwrap()
    std::env::var("APP_MODE").expect("configured")
    "#
}

fn parse_with_context(raw: &str) -> Result<u16, std::num::ParseIntError> {
    raw.parse::<u16>()
}

fn parse_inferred_with_context(raw: &str) -> Result<u16, std::num::ParseIntError> {
    raw.parse()
}

fn read_mode() -> String {
    std::env::var("APP_MODE").unwrap_or_else(|_| "development".to_string())
}

fn notes() {
    // env::var("SECRET").unwrap() should stay documentation, not executable code.
    let _ = documentation_mentions_only();
}
