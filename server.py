#!/usr/bin/env python3
"""Vestel Smart TV network remote — local web UI."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

TV_IP = "192.168.1.104"
REMOTE_PORT = 56791
DISCOVERY_PORT = 56792
HOST = "127.0.0.1"
PORT = 8765

KEYS = {
    "power": 1012,
    "mute": 1013,
    "vol_up": 1016,
    "vol_down": 1017,
    "ch_up": 1032,
    "ch_down": 1033,
    "up": 1020,
    "down": 1019,
    "left": 1021,
    "right": 1022,
    "ok": 1053,
    "back": 1010,
    "exit": 1037,
    "menu": 1048,
    "qmenu": 1043,
    "source": 1056,
    "info": 1018,
    "internet": 1046,
    "epg": 1047,
    "home": 1046,
    "netflix": "Netflix",
    "youtube": "YouTube",
    "0": 1000,
    "1": 1001,
    "2": 1002,
    "3": 1003,
    "4": 1004,
    "5": 1005,
    "6": 1006,
    "7": 1007,
    "8": 1008,
    "9": 1009,
    "red": 1055,
    "green": 1054,
    "yellow": 1050,
    "blue": 1052,
    "play": 1025,
    "pause": 1049,
    "stop": 1024,
    "rew": 1027,
    "ff": 1028,
}

INDEX_HTML = Path(__file__).with_name("index.html").read_text(encoding="utf-8")


def send_key(code: int | str) -> dict:
    if isinstance(code, str):
        url = f"http://{TV_IP}:{REMOTE_PORT}/apps/{code}"
        data = b""
    else:
        url = f"http://{TV_IP}:{REMOTE_PORT}/apps/vr/remote"
        xml = f'<?xml version="1.0" ?><remote><key code="{code}"/></remote>'
        data = xml.encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            return {"ok": True, "status": resp.status}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "error": str(exc.reason)}
    except Exception as exc:  # noqa: BLE001 — surface any network failure to UI
        return {"ok": False, "error": str(exc)}


def tv_status() -> dict:
    url = f"http://{TV_IP}:{DISCOVERY_PORT}/dd.xml"
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            body = resp.read(800).decode("utf-8", errors="replace")
            return {"ok": True, "ip": TV_IP, "detail": "TV yanıt verdi", "snippet": body[:200]}
    except Exception:
        # Fallback: try remote endpoint
        try:
            req = urllib.request.Request(
                f"http://{TV_IP}:{REMOTE_PORT}/apps/vr/remote",
                data=b"",
                method="POST",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            with urllib.request.urlopen(req, timeout=2) as resp:
                return {"ok": True, "ip": TV_IP, "detail": f"Port {REMOTE_PORT} açık", "status": resp.status}
        except urllib.error.HTTPError as exc:
            # HTTP response means host is up
            return {"ok": True, "ip": TV_IP, "detail": f"TV erişilebilir (HTTP {exc.code})"}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "ip": TV_IP, "error": str(exc)}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        print(f"[remote] {args[0]}")

    def _json(self, payload: dict, status: int = 200) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            raw = INDEX_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        if self.path == "/api/status":
            self._json(tv_status())
            return
        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/key":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        name = str(body.get("key", ""))
        if name not in KEYS:
            self._json({"ok": False, "error": f"Bilinmeyen tuş: {name}"}, 400)
            return
        self._json(send_key(KEYS[name]))


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Vestel kumanda hazır → http://{HOST}:{PORT}")
    print(f"TV hedefi: {TV_IP}:{REMOTE_PORT}")
    print("Durdurmak için Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKapatıldı.")


if __name__ == "__main__":
    main()
