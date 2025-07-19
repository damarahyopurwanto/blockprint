import argparse
import requests
from blockprint.fingerprint import generate_fingerprint

def fetch_eth_block(block_number):
    url = f"https://api.blockcypher.com/v1/eth/main/blocks/{block_number}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return {
            'number': data['height'],
            'hash': data['hash'],
            'tx_count': len(data.get('txids', [])),
            'timestamp': data.get('time')
        }
    else:
        raise RuntimeError("Failed to fetch block data")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--block', type=int, required=True)
    parser.add_argument('--chain', type=str, choices=['ethereum'], default='ethereum')
    parser.add_argument('--style', type=str, choices=['ascii', 'svg'], default='ascii')
    args = parser.parse_args()

    block = fetch_eth_block(args.block)
    output = generate_fingerprint(block, style=args.style)
    print(output)
