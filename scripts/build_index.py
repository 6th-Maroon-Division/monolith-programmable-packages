import hashlib
import json
import os
from pathlib import Path

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def semver_key(v: str):
    parts = v.split(".")
    if len(parts) != 3:
        return (0, 0, 0)
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return (0, 0, 0)

def main():
    root = Path("packages")
    index = {"packages": {}}

    if not root.exists():
        Path("index").mkdir(parents=True, exist_ok=True)
        Path("index/index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
        return

    for pkg_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        pkg_name = pkg_dir.name
        versions = []
        for ver_dir in sorted([p for p in pkg_dir.iterdir() if p.is_dir()]):
            version = ver_dir.name
            lib = ver_dir / "lib.lua"
            deps = ver_dir / "dependencies.txt"
            meta = ver_dir / "meta.yml"
            if not (lib.exists() and deps.exists() and meta.exists()):
                continue
            versions.append({
                "version": version,
                "path": str(lib).replace("\\", "/"),
                "dependenciesPath": str(deps).replace("\\", "/"),
                "metaPath": str(meta).replace("\\", "/"),
                "libSha256": sha256_file(lib),
                "depsSha256": sha256_file(deps),
                "metaSha256": sha256_file(meta),
            })

        if not versions:
            continue

        versions.sort(key=lambda x: semver_key(x["version"]))
        index["packages"][pkg_name] = {
            "latest": versions[-1]["version"],
            "versions": versions
        }

    Path("index").mkdir(parents=True, exist_ok=True)
    Path("index/index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print("Wrote index/index.json")

if __name__ == "__main__":
    main()
