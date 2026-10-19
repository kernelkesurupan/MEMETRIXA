import re

from app.scanner.net import NetError, request_json

DEX_URL = "https://api.dexscreener.com/latest/dex/tokens/{}"
BASE58_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")


def is_valid_address(address):
    """Alamat Solana = base58, panjang 32-44 karakter."""
    return bool(BASE58_RE.match(address or ""))


def looks_sensitive(text):
    """Deteksi input yang kemungkinan private key / seed phrase."""
    text = (text or "").strip()
    if len(text.split()) >= 12:  # seed phrase 12/24 kata
        return True
    if len(text) >= 60 and re.fullmatch(r"[1-9A-HJ-NP-Za-km-z]+", text):  # private key base58
        return True
    return False


def get_token_pairs(address, top=3):
    """Return list pair Solana (likuiditas tertinggi dulu). Raise NetError jika gagal."""
    if not is_valid_address(address):
        raise NetError("Format alamat mint Solana tidak valid.")

    data = request_json(DEX_URL.format(address))
    pairs = data.get("pairs") if isinstance(data, dict) else None
    if not isinstance(pairs, list):
        return []

    clean = []
    for p in pairs:
        if not isinstance(p, dict) or p.get("chainId") != "solana":
            continue
        base = (p.get("baseToken") or {}).get("address")
        if base != address:  # abaikan pair di mana token hanya jadi quote
            continue
        clean.append(p)

    def liq(p):
        try:
            return float((p.get("liquidity") or {}).get("usd") or 0)
        except (TypeError, ValueError):
            return 0.0

    clean.sort(key=liq, reverse=True)
    return clean[: max(1, top)]
