"""
Minimal backend server for the HAProxy demo.

Uses only the Python standard library — no pip installs, no extra layers —
so the Docker image stays small and there's nothing external to break.

Each container prints its own NODE_NAME so it's easy to see, from the
outside, which backend actually served a given request.
"""

import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Dedicated health check endpoint — kept separate from "/" so that
        # HAProxy's health checks never depend on real application logic.
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            return

        # NODE_NAME is injected via docker-compose.yml (one per service).
        # Falls back to the container's hostname if it's ever unset.
        node = os.environ.get("NODE_NAME", socket.gethostname())
        body = f"Hello from {node}\n".encode()

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Suppress default per-request console logging to keep
        # `docker compose logs` readable during testing.
        pass


if __name__ == "__main__":
    # Binds to all interfaces so it's reachable from other containers
    # on the same Docker network, not just from inside itself.
    HTTPServer(("0.0.0.0", 5000), Handler).serve_forever()