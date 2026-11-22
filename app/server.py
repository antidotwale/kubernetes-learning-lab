import json
import os
import signal
import socket
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STARTED = time.time()
DELAY = float(os.environ.get("STARTUP_DELAY", "0"))
VERSION = os.environ.get("VERSION", "v1")
MESSAGE = os.environ.get("MESSAGE", "hello from kubelab")


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, "ok", "text/plain")
        elif self.path == "/readyz":
            if time.time() - STARTED >= DELAY:
                self._send(200, "ready", "text/plain")
            else:
                self._send(503, "starting", "text/plain")
        elif self.path == "/":
            info = {"app": "kubelab", "version": VERSION, "message": MESSAGE, "pod": socket.gethostname()}
            self._send(200, json.dumps(info))
        else:
            self._send(404, "not found", "text/plain")


def stop(signum, frame):
    print("signal received, shutting down", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, stop)
    print("kubelab " + VERSION + " listening on 8080", flush=True)
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
