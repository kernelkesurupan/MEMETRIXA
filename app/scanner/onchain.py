import os

from app.scanner.net import NetError, request_json

DEFAULT_RPC = "https://api.mainnet-beta.solana.com"


def _rpc_url():
    url = os.environ.get("MEMETRIXA_RPC", DEFAULT_RPC).strip()
    return url if url.lower().startswith("https://") else DEFAULT_RPC


def _rpc(method, params):
    res = request_json(
        _rpc_url(),
        {"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
    )
    if not isinstance(res, dict) or "error" in res:
        raise NetError("RPC error")
    return res.get("result")


def get_onchain_info(mint):
    """Return dict. Key 'available' False jika RPC gagal (scan tetap jalan)."""
    info = {"available": False}
    try:
        acc = _rpc("getAccountInfo", [mint, {"encoding": "jsonParsed"}])
        value = (acc or {}).get("value")
        data = (value or {}).get("data")
        parsed = data.get("parsed") if isinstance(data, dict) else None
        if not parsed or parsed.get("type") != "mint":
            return info

        i = parsed.get("info") or {}
        decimals = int(i.get("decimals") or 0)
        supply = int(i.get("supply") or 0) / (10 ** decimals) if decimals >= 0 else 0

        info.update(
            available=True,
            mint_authority=i.get("mintAuthority"),
            freeze_authority=i.get("freezeAuthority"),
            supply=supply,
            decimals=decimals,
            top1_pct=None,
            top10_pct=None,
        )
    except (NetError, ValueError, TypeError, AttributeError):
        return info

    # Konsentrasi holder (opsional; gagal tidak membatalkan hasil lain)
    try:
        res = _rpc("getTokenLargestAccounts", [mint])
        accounts = (res or {}).get("value") or []
        amounts = [float(a.get("uiAmount") or 0) for a in accounts]
        if info["supply"] > 0 and amounts:
            info["top1_pct"] = amounts[0] / info["supply"] * 100
            info["top10_pct"] = sum(amounts[:10]) / info["supply"] * 100
    except (NetError, ValueError, TypeError, AttributeError):
        pass

    return info
