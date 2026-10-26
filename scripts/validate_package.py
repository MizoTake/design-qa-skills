"""Validate this repository's portable skill packages using the standard library."""

import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


SKILL_NAMES = ("design", "qa")
LINK = re.compile(r"!?\[[^\]\n]*\]\((?:<([^>\n]+)>|([^\s)]+))\)")
LOCAL_PATH = re.compile(r"(?<!\w)[A-Za-z]:[\\/]|\\\\[^\s\\]+\\|(?<![\w:/])/(?:Users|home|mnt|tmp|var|opt|private|workspace)/")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def read_utf8(path, errors):
    try:
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{path}: unexpected UTF-8 BOM in new package")
        return raw.decode("utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeError) as error:
        errors.append(f"{path}: cannot read UTF-8: {error}")
        return None


def check_links(path, content, boundary, errors):
    for match in LINK.finditer(content):
        link = match.group(1) or match.group(2)
        try:
            parsed = urlsplit(link)
        except ValueError as error:
            errors.append(f"{path}: invalid link: {link}: {error}")
            continue
        if parsed.scheme in ("https", "http", "mailto"):
            continue
        relative_path = unquote(parsed.path)
        if (
            parsed.scheme
            or parsed.netloc
            or relative_path.startswith(("/", "\\"))
            or "\\" in relative_path
            or re.match(r"[A-Za-z]:", relative_path)
        ):
            errors.append(f"{path}: non-portable link: {link}")
            continue
        try:
            target = (path.parent / relative_path).resolve()
        except (OSError, ValueError) as error:
            errors.append(f"{path}: invalid link target: {link}: {error}")
            continue
        if not target.is_relative_to(boundary.resolve()):
            errors.append(f"{path}: link escapes package: {link}")
        elif not target.exists():
            errors.append(f"{path}: missing link target: {link}")


def check_frontmatter(path, content, errors):
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", content, re.DOTALL)
    if match is None:
        errors.append(f"{path}: missing or malformed frontmatter")
        return
    fields = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator or key in fields:
            errors.append(f"{path}: invalid or duplicate metadata field: {line}")
            continue
        fields[key] = value.strip()
    if set(fields) != {"name", "description"}:
        errors.append(f"{path}: expected name and description fields")
    name = fields.get("name", "")
    if not NAME.fullmatch(name) or len(name) > 64 or name != path.parent.name:
        errors.append(f"{path}: invalid name or folder mismatch: {name}")
    try:
        # A constrained YAML subset keeps validation independent of a YAML runtime.
        description = json.loads(fields.get("description", ""))
    except (ValueError, TypeError):
        description = None
    if (
        not isinstance(description, str)
        or not description.strip()
        or len(description) > 1024
        or "TODO" in description
        or any(character in description for character in "<>\n\r")
    ):
        errors.append(f"{path}: description must be a non-empty JSON-quoted YAML string (max 1024 characters)")
    if not match.group(2).strip():
        errors.append(f"{path}: skill body is empty")


def validate_skill(folder):
    folder = Path(folder).resolve()
    errors = []
    entrypoint = folder / "SKILL.md"
    if not entrypoint.is_file():
        return [f"{entrypoint}: missing entrypoint"]
    for path in sorted(folder.rglob("*.md")):
        if not path.resolve().is_relative_to(folder):
            errors.append(f"{path}: file escapes package")
            continue
        content = read_utf8(path, errors)
        if content is None:
            continue
        if path == entrypoint:
            check_frontmatter(path, content, errors)
        if LOCAL_PATH.search(content):
            errors.append(f"{path}: local absolute path in portable skill")
        check_links(path, content, folder, errors)
    return errors


def validate_repository(root):
    root = Path(root).resolve()
    errors = []
    for name in SKILL_NAMES:
        errors.extend(validate_skill(root / "skills" / name))
    for filename in ("README.md", "README.en.md", "CHANGELOG.md", "evals/README.md"):
        path = root / filename
        content = read_utf8(path, errors)
        if content is not None:
            check_links(path, content, root, errors)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    arguments = parser.parse_args()
    errors = validate_repository(arguments.root)
    for error in errors:
        print(error)
    if errors:
        return 1
    print("Package validation passed (design, qa).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
