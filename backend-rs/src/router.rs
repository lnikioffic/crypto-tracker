use axum::{
    Router,
    http::{HeaderValue, Method},
    middleware::from_fn,
    routing::get,
};
use tower_http::cors::CorsLayer;

use crate::{
    api::{get_coin, get_coins_list},
    middleware::tracing_middleware,
};

pub async fn get_app() -> Router {
    let cors = CorsLayer::new()
        // какие домены разрешены
        .allow_origin([
            "http://localhost:5173".parse::<HeaderValue>().unwrap(),
            "https://myapp.com".parse::<HeaderValue>().unwrap(),
        ])
        .allow_credentials(true)
        .allow_methods([Method::GET, Method::POST])
        .allow_headers([
            "content-type".parse().unwrap(),
            "authorization".parse().unwrap(),
        ]);

    Router::new()
        .route("/alive", get(|| async { "ok" }))
        .nest(
            "/coins/",
            Router::new()
                .route("/", get(get_coins_list))
                .route("/{ids}", get(get_coin)),
        )
        .layer(cors)
        .layer(from_fn(tracing_middleware))
}
