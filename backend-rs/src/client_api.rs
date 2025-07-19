use std::collections::HashMap;

use reqwest::{Client, Response, header};

pub struct HttpClient {
    inner: Client,
    base_url: String,
}

impl HttpClient {
    pub fn new(base_ulr: String, headers: HashMap<String, String>) -> Self {
        let mut default_headers = header::HeaderMap::new();
        for (k, v) in headers {
            default_headers.insert(
                header::HeaderName::from_bytes(k.as_bytes()).unwrap(),
                header::HeaderValue::from_str(&v).unwrap(),
            );
        }
        let inner = Client::builder()
            .default_headers(default_headers)
            .build()
            .unwrap();

        Self {
            inner,
            base_url: base_ulr,
        }
    }

    pub async fn get_response(
        &self,
        path: &str,
        params: Option<HashMap<&str, &str>>,
    ) -> Result<Response, Box<dyn std::error::Error>> {
        let url = format!("{}{}", self.base_url, path);

        let mut req = self.inner.get(&url);
        if let Some(p) = params {
            req = req.query(&p);
        }

        let resp = req.send().await?.error_for_status()?;
        Ok(resp)
    }
}
