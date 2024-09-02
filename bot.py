import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime
import random

init(autoreset=True)

http_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'Origin': 'https://mini-app.tomarket.ai',
    'Referer': 'https://mini-app.tomarket.ai/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.134 Mobile Safari/537.36',
    'X-Requested-With': 'org.telegram.messenger.web'
}

def fetch_balance(auth_token):
    balance_url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/balance'
    http_headers['Authorization'] = auth_token
    try:
        result = requests.get(balance_url, headers=http_headers)
        result.raise_for_status()
        return result.json()
    except requests.exceptions.RequestException as err:
        print(f"✖️ Failed to retrieve balance: {err}")
        return None

def daily_reward(auth_token):
    reward_url = 'https://api-web.tomarket.ai/tomarket-game/v1/daily/claim'
    http_headers['Authorization'] = auth_token
    payload_data = {"game_id": "fa873d13-d831-4d6f-8aee-9cff7a1d0db1"}
    try:
        result = requests.post(reward_url, headers=http_headers, json=payload_data)
        result.raise_for_status()
        return result.json()
    except requests.exceptions.RequestException as err:
        print(f"✖️ Daily reward claim failed: {err}")
        return None

def initiate_farming(auth_token):
    farming_url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/start'
    http_headers['Authorization'] = auth_token
    payload_data = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    try:
        result = requests.post(farming_url, headers=http_headers, json=payload_data)
        result.raise_for_status()
        return result.json()
    except requests.exceptions.RequestException as err:
        print(f"✖️ Unable to start farming: {err}")
        return None

def start_game(auth_token):
    play_url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/play'
    http_headers['Authorization'] = auth_token
    payload_data = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d"}
    try:
        result = requests.post(play_url, headers=http_headers, json=payload_data)
        result.raise_for_status()
        return result.json()
    except requests.exceptions.RequestException as err:
        print(f"✖️ Game start failed: {err}")
        return None

def claim_game_points(auth_token, points):
    claim_url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/claim'
    http_headers['Authorization'] = auth_token
    payload_data = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d", "points": points}
    try:
        result = requests.post(claim_url, headers=http_headers, json=payload_data)
        result.raise_for_status()
        return result.json()
    except requests.exceptions.RequestException as err:
        print(f"✖️ Point claim failed: {err}")
        return None

def main():
    try:
        with open('token.txt', 'r') as file:
            token_list = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"{Fore.RED}⚠️ ERROR: The token file was not found.")
        return

    if not token_list:
        print(f"{Fore.RED}⚠️ WARNING: No tokens available for processing.")
        return

    for idx, token in enumerate(token_list):
        print(f"\n🔹 Account [{idx + 1}/{len(token_list)}]: Processing Initiated")

        balance_info = fetch_balance(token)
        if balance_info:
            balance_amount = balance_info['data'].get('available_balance', 'N/A')
            tickets_available = balance_info['data'].get('play_passes', 'N/A')
            print(f"   💰 Balance: {balance_amount} | 🎫 Tickets: {tickets_available}")
        
            print(f"   📅 Claiming daily reward...")
            daily_info = daily_reward(token)
            if daily_info:
                if daily_info['message'] == 'already_check':
                    print(f"   ✅ Already claimed today.")
                else:
                    print(f"   🏆 Reward claimed successfully!")

            print(f"   🌾 Starting farming...")
            farming_info = initiate_farming(token)
            if farming_info:
                print(f"   🚜 Farming started!")
            else:
                print(f"   ❌ Failed to initiate farming.")

            print(f"   🎮 Starting game...")
            game_info = start_game(token)
            if game_info:
                print(f"   🎯 Game launched! Awaiting results...")
                time.sleep(30)
                random_points = random.randint(400, 600)
                claim_info = claim_game_points(token, random_points)
                if claim_info:
                    print(f"   🥇 Points claimed: {random_points}")
                else:
                    print(f"   ❌ Failed to claim points.")
            else:
                print(f"   ❌ Game could not be started.")
        else:
            print(f"   ⚠️ Balance retrieval failed.")

    print(f"{Fore.BLUE}✨ Processing of all accounts completed. ✨")
    time.sleep(1800)

if __name__ == "__main__":
    main()
