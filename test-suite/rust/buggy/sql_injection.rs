use std::collections::HashMap;

use axum::extract::{Json, Query};
use rusqlite::params;

struct Client;
struct Connection;
struct Pool;
struct Request;

struct Payload {
    status: String,
}

impl Request {
    fn query_string(&self) -> &str {
        "tenant=acme"
    }
}

async fn search_users(Query(params): Query<HashMap<String, String>>, pool: &Pool) {
    let email = match params.get("email") {
        Some(value) => value,
        None => "",
    };
    let sql = format!("SELECT id, email FROM users WHERE email = '{}'", email);
    let _rows = sqlx::query(&sql).fetch_all(pool).await;
}

fn update_status(Json(payload): Json<Payload>, conn: &Connection) {
    let statement = format!("UPDATE accounts SET status = '{}' WHERE id = 42", payload.status);
    let _affected = diesel::sql_query(statement).execute(conn);
}

fn delete_tenant(req: Request, conn: &Connection) {
    let tenant = req.query_string();
    let sql = format!("DELETE FROM tenants WHERE slug = '{}'", tenant);
    let _deleted = conn.execute(&sql, []);
}

fn delete_tenant_with_params_macro(req: Request, conn: &Connection) {
    let tenant = req.query_string();
    let _deleted = conn.execute(
        &format!("DELETE FROM tenants WHERE slug = '{}'", tenant),
        params![],
    );
}

fn append_filter(Query(params): Query<HashMap<String, String>>, client: &Client) {
    let user = params.get("user").cloned().unwrap_or_default();
    let mut query = String::from("SELECT id FROM sessions WHERE user = '");
    query.push_str(&user);
    query.push_str("'");
    let _rows = client.query(&query, &[]);
}
