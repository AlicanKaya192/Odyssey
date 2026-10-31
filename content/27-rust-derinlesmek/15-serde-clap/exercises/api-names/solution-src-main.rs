use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Account {
    user_id: u32,
    #[serde(skip_serializing_if = "Option::is_none")]
    nick_name: Option<String>,
}

fn main() {
    let first = Account { user_id: 1, nick_name: None };
    let second = Account { user_id: 2, nick_name: Some("gh".to_string()) };
    println!("{}", serde_json::to_string(&first).unwrap());
    println!("{}", serde_json::to_string(&second).unwrap());
}
