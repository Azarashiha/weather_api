import requests
import asyncio
import websockets
import base64
import json
import os

# APIキーの設定
API_KEY = "key"

# APIエンドポイント
CONTRACT_URL = "https://api.dmdata.jp/v2/contract"
SOCKET_START_URL = "https://api.dmdata.jp/v2/socket"

# 保存ディレクトリ
SAVE_DIR = "data"

# Basic認証用のヘッダーを作成
def create_auth_header(api_key):
    user_pass = f"{api_key}:"
    basic_base64 = base64.b64encode(user_pass.encode()).decode()
    return {"Authorization": f"Basic {basic_base64}"}

# 契約情報リストを取得
def get_contract_list():
    headers = create_auth_header(API_KEY)
    response = requests.get(CONTRACT_URL, headers=headers)
    return response.json()

# WebSocket接続情報を取得
def start_websocket(classifications):
    headers = create_auth_header(API_KEY)
    body = {
        "classifications": classifications,
        "types": [
            "VXSE51",
            "VXSE52",
            "VXSE53",
            "VPWW54",
            "VXSE44",
            "VXSE45",
            "VXSE43",
            "VTSE41",
            "VTSE51",
            "VZSE40",
            #"IXAC41"

        ],
        "test": "no",
        "appName": "Application Test"
    }
    response = requests.post(SOCKET_START_URL, headers=headers, json=body)
    return response.json()

# WebSocketクライアント
async def websocket_client(url):
    async with websockets.connect(url) as websocket:
        while True:
            response = await websocket.recv()
            response_data = json.loads(response)
            print(f"Received: {response_data}")
            
            # pingに対してpongを返す
            if response_data.get('type') == 'ping':
                await websocket.send(json.dumps({
                    "type": "pong",
                    "pingId": response_data.get('pingId')
                }))
            # dataタイプのメッセージを保存
            elif response_data.get('type') == 'data':
                save_data(response_data)

# データをファイルに保存
def save_data(data):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    file_path = os.path.join(SAVE_DIR, f"{data['id']}.json")
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_path}")

# メイン関数
def main():
    # 契約情報リストを取得
    contract_list = get_contract_list()
    print("Contract List:", contract_list)

    # 有効な契約の分類を抽出
    valid_classifications = [item['classification'] for item in contract_list['items'] if item['isValid']]
    
    if not valid_classifications:
        print("No valid contracts found.")
        return

    # WebSocket接続情報を取得
    websocket_info = start_websocket(valid_classifications)
    print("WebSocket Info:", websocket_info)

    if 'websocket' not in websocket_info:
        print("Failed to start WebSocket connection:", websocket_info)
        return

    # WebSocket接続URLを取得
    websocket_url = websocket_info['websocket']['url']

    # WebSocketクライアントを実行
    asyncio.get_event_loop().run_until_complete(websocket_client(websocket_url))

if __name__ == "__main__":
    main()
