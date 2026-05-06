use std::collections::HashMap;

use axum::extract::{Json, Query};
use rusqlite::params;

struct Connection;
struct Pool;

struct Payload {
    status: String,
}

fn first_param<'a>(params: &'a HashMap<String, String>, name: &str) -> &'a str {
    match params.get(name) {
        Some(value) => value.as_str(),
        None => "",
    }
}

async fn search_users(Query(params): Query<HashMap<String, String>>, pool: &Pool) {
    let email = first_param(&params, "email");
    let _rows = sqlx::query("SELECT id, email FROM users WHERE email = $1")
        .bind(email)
        .fetch_all(pool)
        .await;
}

async fn compile_checked_query(Query(params): Query<HashMap<String, String>>) {
    let email = first_param(&params, "email");
    let _row = sqlx::query!("SELECT id, email FROM users WHERE email = ?", email);
}

fn delete_tenant(Query(params): Query<HashMap<String, String>>, conn: &Connection) {
    let tenant = first_param(&params, "tenant");
    let _deleted = conn.execute("DELETE FROM tenants WHERE slug = ?1", params![tenant]);
}

fn update_status(Json(payload): Json<Payload>, conn: &Connection) {
    use diesel::sql_types::Text;

    let _affected = diesel::sql_query("UPDATE accounts SET status = $1 WHERE id = 42")
        .bind::<Text, _>(payload.status)
        .execute(conn);
}
