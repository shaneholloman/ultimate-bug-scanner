fn interpolated_format(name: &str) -> String {
    format!("hello {name}")
}

fn escaped_brace_format() -> String {
    format!("{{status}}")
}

fn direct_string(input: &str) -> String {
    input.to_string()
}

fn documentation_mentions_only() -> &'static str {
    r#"
    These examples are documentation, not executable allocation smells:
    format!("static label")
    input.to_owned().to_string()
    for item in items { item.clone(); }
    items.iter().collect::<Vec<String>>()
    items.iter().nth(0)
    "#
}

fn notes() {
    // format!("static label") should not count from comments.
    // item.clone(), collect::<Vec<_>>(), and nth(0) should stay documentation.
    let _ = documentation_mentions_only();
}
