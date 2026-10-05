import os
import socket
import ssl
import threading
import time
import webbrowser

# cPanel compatibility:
# Some hosting stacks close Python's IPv6/TLS handshake even though the same
# cPanel hostname works normally in a browser. Prefer IPv4 and TLS 1.2 before
# importing the application so urllib/cPanel use the compatible path.
_original_getaddrinfo = socket.getaddrinfo

def _prisca_ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        result = _original_getaddrinfo(
            host, port, socket.AF_INET, type, proto, flags
        )
        if result:
            return result
    except OSError:
        pass
    return _original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = _prisca_ipv4_getaddrinfo

_original_unverified_context = ssl._create_unverified_context

def _prisca_tls12_context(*args, **kwargs):
    ctx = _original_unverified_context(*args, **kwargs)
    try:
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    except Exception:
        pass
    return ctx

ssl._create_unverified_context = _prisca_tls12_context

# Prevent machine-level proxy settings from hijacking the direct cPanel API.
for _key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(_key, None)

# Explicitly bypass proxies for cPanel/Prisca hosts.
os.environ["NO_PROXY"] = "priscaholidays.com,.priscaholidays.com,localhost,127.0.0.1"
os.environ["no_proxy"] = os.environ["NO_PROXY"]

import app

PORT = int(os.environ.get("PORT", "8765"))

def main():
    app.init_db()
    app.seed_excel()
    app.seed_rainwood()
    app.normalize_price_categories()
    app.seed_cabs()
    server = app.ThreadingHTTPServer(("127.0.0.1", PORT), app.H)
    def open_browser():
        time.sleep(1.2)
        webbrowser.open(f"http://127.0.0.1:{PORT}")
    threading.Thread(target=open_browser, daemon=True).start()
    print(f"Prisca AI V27 running at http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    main()
