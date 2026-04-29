from __future__ import annotations

import sys
from pathlib import Path

import uvicorn


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    root_as_str = str(project_root)
    if root_as_str not in sys.path:
        sys.path.insert(0, root_as_str)

    from src.api.main import app

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
