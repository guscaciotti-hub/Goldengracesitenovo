#!/usr/bin/env python3
"""Sobe a página num servidor local e tira prints em 375px (celular) e 1280px (desktop)."""

import functools
import http.server
import pathlib
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAIDA = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / ".prints"
PORTA = 8899


def servir():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(RAIZ))
    socketserver.TCPServer.allow_reuse_address = True
    servidor = socketserver.TCPServer(("127.0.0.1", PORTA), handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    servidor = servir()
    url = f"http://127.0.0.1:{PORTA}/index.html"

    # o container já traz o Chromium; não baixar outro
    chromium = next(iter(sorted(pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome"))), None)

    with sync_playwright() as p:
        navegador = p.chromium.launch(executable_path=str(chromium) if chromium else None,
                                      args=["--no-sandbox"])

        # ── celular 375 x 667 ──
        ctx = navegador.new_context(viewport={"width": 375, "height": 667},
                                    device_scale_factor=2, is_mobile=True, has_touch=True)
        pagina = ctx.new_page()
        erros = []
        pagina.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
        pagina.on("pageerror", lambda e: erros.append(str(e)))
        pagina.goto(url, wait_until="networkidle")
        pagina.evaluate("document.querySelector('.aviso-dev')?.remove()")
        pagina.wait_for_timeout(400)

        pagina.screenshot(path=SAIDA / "mobile-dobra.png")
        pagina.screenshot(path=SAIDA / "mobile-inteira.png", full_page=True)

        altura = pagina.evaluate("document.body.scrollHeight")
        print(f"altura total mobile: {altura}px")
        print("erros de console:", erros or "nenhum")
        ctx.close()

        # ── desktop 1280 ──
        ctx = navegador.new_context(viewport={"width": 1440, "height": 900})
        pagina = ctx.new_page()
        pagina.goto(url, wait_until="networkidle")
        pagina.evaluate("document.querySelector('.aviso-dev')?.remove()")
        pagina.wait_for_timeout(400)
        pagina.screenshot(path=SAIDA / "desktop-dobra.png")
        pagina.screenshot(path=SAIDA / "desktop-inteira.png", full_page=True)
        ctx.close()

        navegador.close()

    servidor.shutdown()
    for arq in sorted(SAIDA.glob("*.png")):
        print(f"{arq}  {arq.stat().st_size} bytes")


if __name__ == "__main__":
    main()
