# source .venv/bin/activate

import argparse
import fnmatch
from pathlib import Path


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
}

DEFAULT_EXCLUDED_FILES = {
    "loki-values-default.yaml",
    "generate_structure.py",
    ".gitignore",
    "structure.md",
    "*postman_collection.json",
    ".DS_Store",
    "*.md",
    "*.txt",
    "*.html",
}


def is_excluded_file(path: Path, excluded_files: set[str]) -> bool:
    """Return True if the file matches any exclusion pattern."""
    return any(
        fnmatch.fnmatch(path.name, pattern)
        for pattern in excluded_files
    )


def is_binary_file(path: Path) -> bool:
    """Return True if the file appears to be binary."""
    try:
        data = path.read_bytes()[:8192]
        return b"\x00" in data
    except (OSError, PermissionError):
        return True


def build_tree(
    root: Path,
    excluded_dirs: set[str],
    excluded_files: set[str],
) -> list[str]:
    """Build a Markdown-style directory tree."""
    lines = [f"{root.name}/"]

    def walk(directory: Path, prefix: str = ""):
        try:
            entries = sorted(
                directory.iterdir(),
                key=lambda p: (p.is_file(), p.name.lower()),
            )
        except (OSError, PermissionError):
            return

        entries = [
            entry
            for entry in entries
            if not (
                (entry.is_dir() and entry.name in excluded_dirs)
                or (
                    entry.is_file()
                    and is_excluded_file(entry, excluded_files)
                )
            )
        ]

        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1
            connector = "└── " if is_last else "├── "

            lines.append(
                prefix
                + connector
                + entry.name
                + ("/" if entry.is_dir() else "")
            )

            if entry.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                walk(entry, new_prefix)

    walk(root)
    return lines


def collect_files(
    root: Path,
    excluded_dirs: set[str],
    excluded_files: set[str],
) -> list[Path]:
    """Collect all text files recursively."""
    files = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        relative_parts = path.relative_to(root).parts

        if any(part in excluded_dirs for part in relative_parts[:-1]):
            continue

        if is_excluded_file(path, excluded_files):
            continue

        if is_binary_file(path):
            continue

        files.append(path)

    return files


def read_file(path: Path) -> str:
    """Read a text file safely."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, PermissionError) as exc:
        return f"[Unable to read file: {exc}]"


def generate_structure(root: Path) -> str:
    excluded_dirs = DEFAULT_EXCLUDED_DIRS
    excluded_files = DEFAULT_EXCLUDED_FILES

    tree = build_tree(
        root,
        excluded_dirs,
        excluded_files,
    )

    files = collect_files(
        root,
        excluded_dirs,
        excluded_files,
    )

    sections = []

    # ------------------------------------------------------------------
    # 1. Directory tree
    # ------------------------------------------------------------------

    sections.append("# 1. Directory tree\n\n")
    sections.append("```text\n")
    sections.extend(line + "\n" for line in tree)
    sections.append("```\n\n")

    # ------------------------------------------------------------------
    # 2. File contents
    # ------------------------------------------------------------------

    sections.append("# 2. Files and contents\n\n")

    for path in files:
        relative_path = path.relative_to(root)

        sections.append(f"## `{relative_path}`\n\n")

        content = read_file(path)

        # Use a generic code block so that the original file contents
        # don't accidentally terminate the Markdown code block.
        sections.append("```\n")
        sections.append(content)

        if content and not content.endswith("\n"):
            sections.append("\n")

        sections.append("```\n\n")

    return "".join(sections)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Markdown representation of a directory structure and file contents."
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to process. Defaults to current directory.",
    )

    args = parser.parse_args()

    root = Path(args.directory).resolve()

    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    output_file = root / "structure.md"

    content = generate_structure(root)

    output_file.write_text(
        content,
        encoding="utf-8",
    )

    print(f"Structure generated: {output_file}")


if __name__ == "__main__":
    main()