import hashlib
import json
import os
from pathlib import Path


def parse_meta_abi(meta_path: Path):
    min_abi = None
    max_abi = None

    with meta_path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("minAbi:"):
                value = line.split(":", 1)[1].strip().strip('"').strip("'")
                try:
                    min_abi = int(value)
                except ValueError:
                    min_abi = None
                continue

            if line.startswith("maxAbi:"):
                value = line.split(":", 1)[1].strip().strip('"').strip("'")
                try:
                    max_abi = int(value)
                except ValueError:
                    max_abi = None

    return min_abi, max_abi

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
            min_abi, max_abi = parse_meta_abi(meta)

            version_entry = {
                "version": version,
                "path": str(lib).replace("\\", "/"),
                "dependenciesPath": str(deps).replace("\\", "/"),
                "metaPath": str(meta).replace("\\", "/"),
                "libSha256": sha256_file(lib),
                "depsSha256": sha256_file(deps),
                "metaSha256": sha256_file(meta),
            }

            if min_abi is not None:
                version_entry["minAbi"] = min_abi
            if max_abi is not None:
                version_entry["maxAbi"] = max_abi

            versions.append(version_entry)

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
