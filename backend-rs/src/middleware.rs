use std::time::Instant;

use axum::{
    body::Body,
    extract::Request,
    http::{HeaderValue, Response},
    middleware::Next,
};
use tracing::info;

pub async fn tracing_middleware(request: Request, next: Next) -> Response<Body> {
    let start = Instant::now();
    let method = request.method().clone();
    let path = request.uri().path().to_owned();

    let response = next.run(request).await;

    let elapsed = start.elapsed().as_secs_f64();
    info!("{method} {path} processed in {elapsed:.4}s");

    let mut response = response;
    response.headers_mut().insert(
        "X-Process-Time",
        HeaderValue::from_str(&elapsed.to_string()).unwrap(),
    );

    response
}
