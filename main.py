"""Memetrixa v2 - Solana Token Risk Scanner | by kernelkesurupan"""
import argparse
import json
import sys
import time

from app import ui
from app.scanner.market_data import get_token_pairs, is_valid_address, looks_sensitive
from app.scanner.net import NetError
from app.scanner.onchain import get_onchain_info
from app.scanner.risk_scanner import analyze_pair

QUIT_WORDS = {"q", "quit", "exit", "keluar"}


def scan(address, args):
    """Scan satu token. Return list hasil (kosong jika gagal)."""
    if looks_sensitive(address):
        print(ui.c("\n ⛔ Input itu terlihat seperti PRIVATE KEY / SEED PHRASE!", "bold", "red"))
        print(ui.c("    Jangan pernah membagikannya. Input dibuang dan tidak disimpan.", "red"))
        print(ui.c("    Jika sudah terlanjur terekspos, pindahkan aset ke wallet baru.\n", "red"))
        return []

    if not is_valid_address(address):
        print(ui.c("\n ✖ Format alamat tidak valid (base58, 32-44 karakter).\n", "red"))
        return []

    print(ui.c("\n ⏳ Mengambil data token...", "cyan"))
    try:
        pairs = get_token_pairs(address, top=args.top)
    except NetError as e:
        print(ui.c(f"\n ✖ {e}\n", "red"))
        return []

    if not pairs:
        print(ui.c("\n ✖ Token tidak ditemukan di DexScreener (belum ada pair / alamat salah).\n", "red"))
        return []

    onchain = None
    if not args.no_onchain:
        print(ui.c(" ⏳ Memeriksa data on-chain (authority & holder)...", "cyan"))
        onchain = get_onchain_info(address)

    print()
    results = []
    for i, pair in enumerate(pairs, 1):
        result = analyze_pair(pair, onchain)
        results.append(result)
        ui.print_report(result, i, len(pairs))
        print()

    if len(results) > 1:
        worst = max(results, key=lambda r: r["score"])
        print(ui.c(f" Skor tertinggi dari {len(results)} pair: {worst['score']}/100 "
                   f"({worst['risk']})\n", "bold"))
    return results


def export_json(path, address, results):
    payload = {
        "tool": "Memetrixa", "version": ui.VERSION, "author": ui.AUTHOR,
        "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "address": address, "results": results,
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(ui.c(f" ✔ Hasil disimpan ke {path}\n", "green"))
    except OSError as e:
        print(ui.c(f" ✖ Gagal menyimpan file: {e}\n", "red"))


def interactive(args):
    ui.banner()
    ui.security_notice()
    print(ui.c(" Ketik alamat mint token Solana (atau 'q' untuk keluar).\n", "dim"))
    while True:
        try:
            raw = input(ui.c(" ➤ Mint address: ", "bold", "cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if raw.lower() in QUIT_WORDS:
            break
        if not raw:
            print(ui.c(" Alamat token tidak boleh kosong.\n", "yellow"))
            continue
        results = scan(raw, args)
        if results and args.json:
            export_json(args.json, raw, results)
    ui.footer()


def parse_args():
    p = argparse.ArgumentParser(description="Memetrixa v2 - Solana Risk Scanner (by kernelkesurupan)")
    p.add_argument("address", nargs="?", help="alamat mint token (kosongkan untuk mode interaktif)")
    p.add_argument("--top", type=int, default=3, choices=range(1, 11), metavar="N",
                   help="jumlah pair teratas yang dianalisis (1-10, default 3)")
    p.add_argument("--json", metavar="FILE", help="simpan hasil ke file JSON")
    p.add_argument("--no-onchain", action="store_true", help="lewati pemeriksaan on-chain")
    p.add_argument("--no-color", action="store_true", help="matikan warna")
    return p.parse_args()


def main():
    args = parse_args()
    if args.no_color:
        ui.set_color(False)

    try:
        if args.address:
            ui.banner()
            results = scan(args.address.strip(), args)
            if results and args.json:
                export_json(args.json, args.address, results)
            ui.footer()
            return 0 if results else 1
        interactive(args)
        return 0
    except KeyboardInterrupt:
        print(ui.c("\n Dihentikan oleh pengguna.", "yellow"))
        return 130


if __name__ == "__main__":
    sys.exit(main())
