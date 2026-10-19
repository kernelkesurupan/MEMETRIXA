import os
import re
import sys

AUTHOR = "kernelkesurupan"
VERSION = "2.0"
W = 64

_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_CODES = {
    "reset": "0", "bold": "1", "dim": "2",
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "white": "97",
}
_enabled = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
if _enabled and os.name == "nt":
    os.system("")  # aktifkan ANSI di Windows terminal


def set_color(flag):
    global _enabled
    _enabled = bool(flag)


def c(text, *styles):
    if not _enabled:
        return str(text)
    codes = ";".join(_CODES[s] for s in styles)
    return f"\x1b[{codes}m{text}\x1b[0m"


def _vlen(s):
    return len(_ANSI.sub("", s))


def _pad(s, width):
    return s + " " * max(0, width - _vlen(s))


def top():
    print(c("╔" + "═" * (W - 2) + "╗", "cyan"))


def mid():
    print(c("╠" + "═" * (W - 2) + "╣", "cyan"))


def bottom():
    print(c("╚" + "═" * (W - 2) + "╝", "cyan"))


def _row(text):
    inner = W - 4
    print(c("║", "cyan") + " " + _pad(text, inner) + " " + c("║", "cyan"))


def _center(text, styles):
    inner = W - 4
    pad_total = inner - len(text)
    left = pad_total // 2
    _row(" " * left + c(text, *styles) + " " * (pad_total - left))


def banner():
    top()
    _center("M E M E T R I X A", ("bold", "cyan"))
    _center("SOLANA TOKEN RISK SCANNER  v" + VERSION, ("white",))
    _center("by " + AUTHOR, ("magenta",))
    bottom()


def security_notice():
    print(c(" 🔒 KEAMANAN", "bold", "yellow"))
    print(c("  • Scanner ini TIDAK pernah meminta private key / seed phrase.", "dim"))
    print(c("  • Jangan masukkan kunci wallet di mana pun. Hanya alamat mint token.", "dim"))
    print(c("  • Hasil bukan saran finansial. Skor rendah ≠ pasti aman (DYOR).", "dim"))
    print()


def risk_color(category):
    return {"RENDAH": "green", "SEDANG": "yellow",
            "TINGGI": "red", "SANGAT TINGGI": "red"}.get(category, "white")


def risk_bar(score, width=30):
    filled = round(score / 100 * width)
    col = "green" if score < 20 else "yellow" if score < 40 else "red"
    return c("█" * filled, col) + c("░" * (width - filled), "dim")


def usd(n):
    if n is None:
        return "-"
    if 0 < abs(n) < 0.01:
        return f"${n:.8f}".rstrip("0")
    if abs(n) >= 1_000_000_000:
        return f"${n/1e9:,.2f}B"
    if abs(n) >= 1_000_000:
        return f"${n/1e6:,.2f}M"
    return f"${n:,.2f}"


def age(hours):
    if hours is None:
        return "tidak diketahui"
    if hours < 1:
        return f"{hours*60:.0f} menit"
    if hours < 48:
        return f"{hours:.1f} jam"
    return f"{hours/24:.1f} hari"


def pct(n):
    col = "green" if n > 0 else "red" if n < 0 else "white"
    return c(f"{n:+.2f}%", col)


def _short(addr):
    return addr if len(addr) <= 20 else addr[:8] + "…" + addr[-8:]


def print_report(r, index=1, total=1):
    top()
    _row(c(f"{r['name']} ", "bold", "white") + c(f"({r['symbol']})", "cyan")
         + c(f"   pair {index}/{total}", "dim"))
    mid()
    rows = [
        ("Mint", _short(r["address"])),
        ("DEX", r["dex"]),
        ("Harga", usd(r["price_usd"])),
        ("Likuiditas", usd(r["liquidity"])),
        ("Volume 24h", usd(r["volume_24h"])),
        ("FDV", usd(r["fdv"])),
        ("Umur pair", age(r["age_hours"])),
        ("Perubahan", f"1j {pct(r['change_1h'])}   24j {pct(r['change_24h'])}"),
        ("Tx 24h", f"{c(r['buys_24h'], 'green')} buy / {c(r['sells_24h'], 'red')} sell"),
    ]
    oc = r["onchain"]
    if oc:
        rows += [
            ("Mint auth", c("AKTIF", "red") if oc.get("mint_authority") else c("dicabut", "green")),
            ("Freeze auth", c("AKTIF", "red") if oc.get("freeze_authority") else c("dicabut", "green")),
        ]
        if oc.get("top1_pct") is not None:
            rows.append(("Top 1 / 10", f"{oc['top1_pct']:.1f}% / {oc['top10_pct']:.1f}%"))
    for k, v in rows:
        _row(c(f"{k:<12}", "dim") + ": " + str(v))

    mid()
    col = risk_color(r["risk"])
    _row(c("SKOR RISIKO ", "bold") + c(f"{r['score']}/100", "bold", col)
         + "  " + c(r["risk"], "bold", col))
    _row(risk_bar(r["score"]))

    if r["warnings"]:
        mid()
        _row(c("PERINGATAN", "bold", "red"))
        for w in r["warnings"]:
            _wrap_rows("▲ ", w, "yellow")
    if r["positives"]:
        mid()
        _row(c("INDIKATOR POSITIF", "bold", "green"))
        for p in r["positives"]:
            _wrap_rows("✓ ", p, "green")
    if r["url"]:
        mid()
        _row(c("Chart: ", "dim") + r["url"][: W - 14])
    bottom()


def _wrap_rows(prefix, text, color):
    inner = W - 4 - len(prefix)
    words, cur, out = text.split(), "", []
    for w in words:
        if len(cur) + len(w) + 1 > inner:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    for i, ln in enumerate(out):
        lead = prefix if i == 0 else " " * len(prefix)
        _row(c(lead, color) + ln)


def footer():
    print(c(f"\n  Memetrixa v{VERSION} • by {AUTHOR} • DYOR, bukan saran finansial\n", "dim"))
