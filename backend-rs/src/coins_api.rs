use std::collections::HashMap;

use chrono::{DateTime, Utc};
use dotenvy::dotenv;
use reqwest::Response;
use serde::{Deserialize, Serialize};

use crate::client_api::HttpClient;

#[derive(Serialize, Deserialize)]
pub struct Coin {
    id: String,
    symbol: String,
    name: String,
    image: String,
    current_price: f64,
    market_cap: f64,
    market_cap_rank: i32,
    fully_diluted_valuation: f64,
    total_volume: Option<f64>,
    high_24h: f64,
    low_24h: f64,
    price_change_24h: f64,
    price_change_percentage_24h: f64,
    circulating_supply: f64,
    total_supply: f64,
    max_supply: Option<f64>,
    last_updated: DateTime<Utc>,
}

pub struct CoinsApi {
    client: HttpClient,
}

impl CoinsApi {
    pub fn new() -> Self {
        dotenv().ok();
        let api_key = std::env::var("COINS_API_KEY").expect("Key must be set");

        let mut headers = HashMap::new();
        headers.insert("accept".to_string(), "application/json".to_string());
        headers.insert("x-cg-demo-api-key".to_string(), api_key);

        Self {
            client: HttpClient::new("https://api.coingecko.com".to_string(), headers),
        }
    }

    // pub async fn get_coins_list(&self) -> Result<Response, Box<dyn std::error::Error>> {
    //     let mut params = HashMap::new();
    //     params.insert("include_platform", "true");
    //     self.client
    //         .get_response("/api/v3/coins/list", Some(params))
    //         .await
    // }

    pub async fn get_coins_markets(
        &self,
        vs_currency: &str,
        extra: Option<HashMap<&str, &str>>,
    ) -> Result<Response, Box<dyn std::error::Error>> {
        let mut params = extra.unwrap_or_default();
        params.insert("vs_currency", vs_currency);

        self.client
            .get_response("/api/v3/coins/markets", Some(params))
            .await
    }
}
