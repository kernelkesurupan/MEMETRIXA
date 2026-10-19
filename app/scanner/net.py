import json
import time
import urllib.error
import urllib.request

MAX_BYTES = 5 * 1024 * 1024  # batas respons 5 MB
MIN_INTERVAL = 0.8           # jeda minimal antar request (detik)
USER_AGENT = "Memetrixa/2.0 (by kernelkesurupan)"

_last_call = 0.0


class NetError(Exception):
    """Error jaringan / API yang sudah dibersihkan untuk ditampilkan ke user."""


class _HttpsOnlyRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not newurl.lower().startswith("https://"):
            raise NetError("Redirect ke koneksi non-HTTPS diblokir.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_opener = urllib.request.build_opener(_HttpsOnlyRedirect)


def request_json(url, payload=None, timeout=10, retries=3):
    global _last_call

    if not url.lower().startswith("https://"):
        raise NetError("Hanya koneksi HTTPS yang diizinkan.")

    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"

    last_err = "unknown"
    for attempt in range(retries):
        wait = MIN_INTERVAL - (time.monotonic() - _last_call)
        if wait > 0:
            time.sleep(wait)
        _last_call = time.monotonic()

        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with _opener.open(req, timeout=timeout) as resp:
                raw = resp.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise NetError("Respons terlalu besar, dibatalkan.")
            return json.loads(raw.decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** attempt)
                continue
            raise NetError(f"Server menolak permintaan ({last_err}).")
        except NetError:
            raise
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = "koneksi gagal / timeout"
            time.sleep(2 ** attempt)
        except (json.JSONDecodeError, UnicodeDecodeError):
            last_err = "respons bukan JSON valid"
            time.sleep(1)

    raise NetError(f"Gagal setelah {retries} percobaan ({last_err}).")
