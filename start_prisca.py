import os
import threading
import time
import webbrowser
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
    print(f"Prisca AI V25 running at http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    main()
