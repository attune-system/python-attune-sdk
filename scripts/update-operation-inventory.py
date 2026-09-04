#!/usr/bin/env python3

import hashlib
import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: update-operation-inventory.py SPEC API_DIR OUTPUT")

    spec_path, api_dir, output_path = map(Path, sys.argv[1:])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    operations = sorted(
        str(path.relative_to(api_dir).with_suffix(""))
        for path in api_dir.glob("*/*.py")
        if path.name != "__init__.py"
    )
    inventory = {
        "source": "attune/web/openapi.json",
        "openapi_info_version": spec["info"]["version"],
        "operation_count": len(operations),
        "sha256": hashlib.sha256("\n".join(operations).encode()).hexdigest(),
    }
    output_path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
