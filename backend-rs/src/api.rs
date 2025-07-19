use std::collections::HashMap;

use axum::{
    Json,
    extract::{Path, Query},
};
use reqwest::StatusCode;
use serde::{Deserialize, Serialize};

use crate::coins_api::{Coin, CoinsApi};

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
enum Currency {
    Usd,
    Rub,
}

impl Currency {
    fn as_str(&self) -> &'static str {
        match self {
            Currency::Usd => "usd",
            Currency::Rub => "rub",
        }
    }
}

pub async fn get_coins_list(
    Query(params): Query<HashMap<String, String>>,
) -> Result<Json<Vec<Coin>>, (StatusCode, String)> {
    let vs_currency = params
        .get("vs_currency")
        .map(|s| {
            if s == "rub" {
                Currency::Rub
            } else {
                Currency::Usd
            }
        })
        .unwrap_or(Currency::Usd);

    let coins_api = CoinsApi::new();
    let response = coins_api
        .get_coins_markets(vs_currency.as_str(), None)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    // Parse the JSON from the successful response
    let coins = response
        .json::<Vec<Coin>>()
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    Ok(Json(coins))
}

pub async fn get_coin(
    Path(id): Path<String>,
    Query(params): Query<HashMap<String, String>>,
) -> Result<Json<Coin>, (StatusCode, String)> {
    if id.contains(',') {
        return Err((
            StatusCode::UNPROCESSABLE_ENTITY,
            "Only one id is allowed".to_string(),
        ));
    }

    let vs_currency = params
        .get("vs_currency")
        .map(|s| {
            if s == "rub" {
                Currency::Rub
            } else {
                Currency::Usd
            }
        })
        .unwrap_or(Currency::Usd);

    // Create extra params HashMap with the coin ID
    let mut extra_params = HashMap::new();
    extra_params.insert("ids", id.as_str());

    let coins_api = CoinsApi::new();
    // Call with both required arguments
    let response = coins_api
        .get_coins_markets(vs_currency.as_str(), Some(extra_params))
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    let mut coins = response
        .json::<Vec<Coin>>()
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    let coin = coins
        .pop()
        .ok_or((StatusCode::NOT_FOUND, "Coin not found".to_string()))?;

    Ok(Json(coin))
}
