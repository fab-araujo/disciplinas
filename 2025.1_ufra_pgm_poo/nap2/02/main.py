import sys
from pathlib import Path

# Garante que o diretório raiz do projeto está no sys.path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.app import BiblioApp

if __name__ == "__main__":
    app = BiblioApp()
    app.run()
