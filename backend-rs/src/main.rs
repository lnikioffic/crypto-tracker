use tracing::{Level, info};

use crate::router::get_app;

mod api;
mod client_api;
mod coins_api;
mod middleware;
mod router;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().with_max_level(Level::INFO).init();

    let app = get_app().await;

    let listener = tokio::net::TcpListener::bind("127.0.0.1:5000")
        .await
        .unwrap();
    info!("Server is running on http://127.0.0.1:5000");
    axum::serve(listener, app).await.unwrap();
}
