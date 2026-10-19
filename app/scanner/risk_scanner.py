"""Mesin skor risiko. Skor 0-100: semakin TINGGI = semakin BERISIKO."""
import re
import time

_CTRL = re.compile(r"[\x00-\x1f\x7f-\x9f\x1b]")


def clean_text(value, limit=40):
    """Data dari API tidak dipercaya: buang karakter kontrol (anti terminal-injection)."""
    text = _CTRL.sub("", str(value or "")).strip()
    return (text[:limit] + "…") if len(text) > limit else (text or "-")


def _f(value, default=0.0):
    try:
        if value is None:
            return default
        x = float(value)
        return x if x == x and abs(x) != float("inf") else default
    except (TypeError, ValueError):
        return default


def categorize(score):
    if score < 20:
        return "RENDAH"
    if score < 40:
        return "SEDANG"
    if score < 60:
        return "TINGGI"
    return "SANGAT TINGGI"


def analyze_pair(pair, onchain=None):
    base = pair.get("baseToken") or {}
    liquidity = _f((pair.get("liquidity") or {}).get("usd"))
    volume = (pair.get("volume") or {})
    vol24 = _f(volume.get("h24"))
    txns = (pair.get("txns") or {}).get("h24") or {}
    buys, sells = int(_f(txns.get("buys"))), int(_f(txns.get("sells")))
    change = pair.get("priceChange") or {}
    ch1, ch24 = _f(change.get("h1")), _f(change.get("h24"))
    fdv = _f(pair.get("fdv"))
    created = _f(pair.get("pairCreatedAt"), None)
    age_h = max(0.0, (time.time() * 1000 - created) / 3_600_000) if created else None
    info = pair.get("info") or {}
    has_web = bool(info.get("websites"))
    has_social = bool(info.get("socials"))

    score, warnings, positives = 0, [], []

    def risk(points, msg):
        nonlocal score
        score += points
        warnings.append(msg)

    # --- Likuiditas ---
    if liquidity < 1_000:
        risk(30, "Likuiditas sangat rendah (<$1K): mudah dimanipulasi & sulit dijual")
    elif liquidity < 5_000:
        risk(22, "Likuiditas rendah (<$5K)")
    elif liquidity < 20_000:
        risk(12, "Likuiditas tergolong kecil (<$20K)")
    elif liquidity < 50_000:
        risk(5, "Likuiditas moderat (<$50K)")
    else:
        positives.append("Likuiditas cukup besar (≥$50K)")

    # --- Umur pair ---
    if age_h is None:
        risk(5, "Umur pair tidak diketahui")
    elif age_h < 1:
        risk(20, "Pair baru dibuat (<1 jam)")
    elif age_h < 24:
        risk(15, "Pair berumur <24 jam")
    elif age_h < 168:
        risk(8, "Pair berumur <7 hari")
    else:
        positives.append("Pair berumur lebih dari 7 hari")

    # --- Volume & aktivitas ---
    if vol24 < 1_000:
        risk(8, "Volume 24 jam sangat sepi (<$1K)")
    if liquidity > 0 and vol24 / liquidity > 20:
        risk(10, "Volume/likuiditas sangat tinggi (>20x): indikasi wash trading / pump")
    total_tx = buys + sells
    if total_tx < 20:
        risk(6, "Jumlah transaksi 24 jam sangat sedikit")
    elif sells > buys * 1.5:
        risk(8, "Tekanan jual dominan (sell jauh lebih banyak dari buy)")

    # --- Pergerakan harga ---
    if ch24 <= -70:
        risk(15, f"Harga anjlok {ch24:.0f}% dalam 24 jam")
    elif ch24 <= -40:
        risk(8, f"Harga turun {ch24:.0f}% dalam 24 jam")
    elif ch24 >= 500:
        risk(8, f"Harga melonjak +{ch24:.0f}% dalam 24 jam (rawan dump)")
    if ch1 <= -30:
        risk(8, f"Harga turun {ch1:.0f}% dalam 1 jam terakhir")

    # --- Valuasi ---
    if liquidity > 0 and fdv / liquidity > 500:
        risk(10, "FDV jauh di atas likuiditas (>500x): harga rapuh")
    elif liquidity > 0 and fdv / liquidity > 100:
        risk(5, "FDV jauh di atas likuiditas (>100x)")

    # --- Kredibilitas proyek ---
    if not has_web and not has_social:
        risk(6, "Tidak ada website maupun sosial media terdaftar")
    else:
        positives.append("Website / sosial media terdaftar")

    # --- On-chain ---
    if onchain and onchain.get("available"):
        if onchain.get("mint_authority"):
            risk(20, "Mint authority AKTIF: dev bisa mencetak token tanpa batas")
        else:
            positives.append("Mint authority dicabut")
        if onchain.get("freeze_authority"):
            risk(15, "Freeze authority AKTIF: dev bisa membekukan wallet kamu")
        else:
            positives.append("Freeze authority dicabut")

        top1, top10 = onchain.get("top1_pct"), onchain.get("top10_pct")
        if top1 is not None:
            if top1 > 50:
                risk(20, f"Holder terbesar menguasai {top1:.1f}% supply")
            elif top1 > 30:
                risk(12, f"Holder terbesar menguasai {top1:.1f}% supply")
            if top10 is not None and top10 > 80:
                risk(10, f"Top 10 holder menguasai {top10:.1f}% supply")
            if top1 <= 30 and (top10 or 0) <= 80:
                positives.append("Distribusi holder tidak terlalu terpusat")
    elif onchain is not None:
        warnings.append("Data on-chain tidak tersedia (RPC gagal), skor kurang akurat")

    score = min(100, score)
    url = pair.get("url") or ""
    return {
        "name": clean_text(base.get("name")),
        "symbol": clean_text(base.get("symbol"), 16),
        "address": clean_text(base.get("address"), 50),
        "dex": clean_text(pair.get("dexId"), 20),
        "pair_address": clean_text(pair.get("pairAddress"), 50),
        "url": url if url.startswith("https://dexscreener.com/") else "",
        "price_usd": _f(pair.get("priceUsd")),
        "liquidity": liquidity,
        "volume_24h": vol24,
        "fdv": fdv,
        "age_hours": age_h,
        "change_1h": ch1,
        "change_24h": ch24,
        "buys_24h": buys,
        "sells_24h": sells,
        "onchain": onchain if onchain and onchain.get("available") else None,
        "score": score,
        "risk": categorize(score),
        "warnings": warnings,
        "positives": positives,
    }


