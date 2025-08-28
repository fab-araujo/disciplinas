import asyncio
import platform
import pygame
from gui import LibraryGUI
from library import Library

# Ponto de entrada assíncrono: inicializa pygame, cria a camada de dados (Library)
# e passa para a GUI (LibraryGUI), que controla o loop da aplicação.
async def main():
    pygame.init()
    library = Library()
    gui = LibraryGUI(library)
    gui.run()

# Suporte a execução no navegador (Emscripten) e local.
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())