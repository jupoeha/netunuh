"""Shiper 部署探针：多端口监听 + 请求/环境回显。纯标准库，零依赖。"""
import os
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MARK = "SHIPER-OK-20260913"
START = time.time()

# 对少数关键变量显示原值，其余只显示变量名（避免把以后注入的密钥类变量公开出去）
SHOW_VALUE = {"PORT", "HOSTNAME", "SHIPER_PORT", "APP_PORT", "NODE_ENV"}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _render(self):
        port = self.server.server_address[1]
        lines = []
        lines.append(f"{MARK}")
        lines.append(f"served_port={port}  uptime_s={int(time.time() - START)}")
        lines.append(f"host={socket.gethostname()}  pid={os.getpid()}  "
                     f"proto={self.request_version}")
        lines.append(f"PORT_env={os.environ.get('PORT')!r}")
        lines.append("env_names=" + ",".join(sorted(os.environ)))
        lines.append("env_values=" + ";".join(
            f"{k}={os.environ[k]}" for k in sorted(SHOW_VALUE & set(os.environ))))
        lines.append(f"method={self.command}  path={self.path!r}")
        lines.append("--- request headers ---")
        for k, v in self.headers.items():
            lines.append(f"{k}: {v}")
        return "\n".join(lines).encode("utf-8", "replace")

    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Served-Port", str(self.server.server_address[1]))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, b"ok\n")
        else:
            self._send(200, self._render())

    def do_HEAD(self):
        self._send(200, b"")

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        n = min(n, 4096)
        body = self.rfile.read(n) if n else b""
        out = self._render() + b"\n--- body(first 4KB) ---\n" + body
        self._send(200, out)

    do_OPTIONS = do_HEAD


def serve(port):
    try:
        httpd = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    except OSError as e:
        print(f"[probe] bind :{port} FAILED: {e}", flush=True)
        return
    print(f"[probe] listening on :{port}", flush=True)
    httpd.serve_forever()


def main():
    ports = []
    p = os.environ.get("PORT", "")
    if p.isdigit():
        ports.append(int(p))
    ports += [8080, 3000, 11622]  # 常见 PaaS 约定端口 + 我们 xhttp 服务的默认端口
    ports = list(dict.fromkeys(ports))
    for q in ports:
        threading.Thread(target=serve, args=(q,), daemon=True).start()
    print(f"[probe] {MARK} starting, trying ports {ports}", flush=True)
    threading.Event().wait()


if __name__ == "__main__":
    main()
