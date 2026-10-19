
import requests

BASE_URL = "https://api.dexscreener.com/token-pairs/v1/solana"


def get_token_pairs(token_address):
    """Mengambil data pool DEX untuk token Solana."""
    url = f"{BASE_URL}/{token_address}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            return []

        return data

    except requests.RequestException as error:
        print(f"Gagal mengambil data: {error}")
        return []


if __name__ == "__main__":
    address = input("Masukkan alamat mint token Solana: ").strip()

    if not address:
        print("Alamat token tidak boleh kosong.")
    else:
        pairs = get_token_pairs(address)

        if not pairs:
            print("Data pool tidak ditemukan atau API sedang bermasalah.")
        else:
            print(f"\nDitemukan {len(pairs)} pool:\n")

            for pair in pairs:
                token = pair.get("baseToken") or {}
                liquidity = pair.get("liquidity") or {}

                print(f"Nama       : {token.get('name', 'Unknown')}")
                print(f"Simbol     : {token.get('symbol', 'Unknown')}")
                print(f"Harga USD  : {pair.get('priceUsd', 'N/A')}")
                print(f"Likuiditas : ${liquidity.get('usd', 0) or 0}")
                print(f"DEX        : {pair.get('dexId', 'Unknown')}")
                print("-" * 35)
