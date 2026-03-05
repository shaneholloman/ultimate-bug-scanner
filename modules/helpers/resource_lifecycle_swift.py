#!/usr/bin/env python3
"""Detect likely Swift resource lifecycle leaks with lightweight code-aware regexes."""
from __future__ import annotations

import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".hg", ".svn", "build", "DerivedData", ".swiftpm", ".idea", "node_modules"}

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"

ASSIGNED_RULES: tuple[tuple[str, str, re.Pattern[str], tuple[re.Pattern[str], ...]], ...] = (
    (
        "timer",
        "Timer is never invalidated",
        re.compile(rf"\b(?:let|var)\s+({IDENT})\s*=\s*(?:try[!?]?\s*)?(?:Timer\.scheduledTimer|Timer\.publish\s*\()"),
        (re.compile(r"\.invalidate\s*\("),),
    ),
    (
        "urlsession_task",
        "URLSession task is never resumed or cancelled",
        re.compile(rf"\b(?:let|var)\s+({IDENT})\s*=\s*(?:try[!?]?\s*)?[^=\n;]*\.(?:dataTask|uploadTask|downloadTask)\s*\("),
        (re.compile(r"\.(?:resume|cancel)\s*\("),),
    ),
    (
        "notification_token",
        "NotificationCenter observer token is never removed",
        re.compile(rf"\b(?:let|var)\s+({IDENT})\s*=\s*NotificationCenter\.default\.addObserver\s*\("),
        (re.compile(r"NotificationCenter\.default\.removeObserver\s*\("), re.compile(r"\.removeObserver\s*\(")),
    ),
    (
        "file_handle",
        "FileHandle is never closed",
        re.compile(rf"\b(?:let|var)\s+({IDENT})\s*=\s*(?:try[!?]?\s*)?FileHandle\s*\(\s*for(?:Reading|Writing|Updating)(?:From|To|AtPath)\s*:"),
        (re.compile(r"\.(?:close|closeFile)\s*\("),),
    ),
    (
        "combine_sink",
        "Combine sink result is neither stored nor cancelled",
        re.compile(rf"\b(?:let|var)\s+({IDENT})\s*=\s*.*?\.sink\s*\(", re.MULTILINE),
        (re.compile(r"\.store\s*\(\s*in:\s*&"), re.compile(r"\.cancel\s*\(")),
    ),
    (
        "dispatch_source",
        "DispatchSource is never resumed or cancelled",
        re.compile(rf"\b(?:let|var)\s+({IDENT})\s*=\s*DispatchSource\.(?:makeTimerSource|makeFileSystemObjectSource|makeReadSource|makeWriteSource)\s*\("),
        (re.compile(r"\.(?:resume|cancel)\s*\("),),
    ),
    (
        "cadisplaylink",
        "CADisplayLink is never invalidated",
        re.compile(rf"\b(?:let|var)\s+({IDENT})\s*=\s*CADisplayLink\s*\("),
        (re.compile(r"\.invalidate\s*\("),),
    ),
)

KVO_RULE = (
    "kvo_observer",
    "KVO observer is added without a matching removeObserver",
    re.compile(r"\baddObserver\s*\([^)]*forKeyPath:"),
    re.compile(r"\bremoveObserver\s*\([^)]*forKeyPath:"),
)


def iter_swiftish_files(root: Path):
    suffixes = {".swift", ".m", ".mm"}
    if root.is_file():
        if root.suffix.lower() in suffixes and not any(part in SKIP_DIRS for part in root.parts):
            yield root
        return
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in suffixes:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def strip_comments_and_strings(text: str) -> str:
    result: list[str] = []
    i = 0
    n = len(text)
    in_line = False
    in_block = False
    in_string = False
    escaped = False
    quote = ""

    def mask_char(ch: str) -> str:
        return "\n" if ch == "\n" else " "

    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""

        if in_line:
            result.append(mask_char(ch))
            if ch == "\n":
                in_line = False
            i += 1
            continue

        if in_block:
            result.append(mask_char(ch))
            if ch == "*" and nxt == "/":
                result.append(" ")
                in_block = False
                i += 2
            else:
                i += 1
            continue

        if in_string:
            result.append(mask_char(ch))
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                in_string = False
            i += 1
            continue

        if ch == "/" and nxt == "/":
            result.extend("  ")
            in_line = True
            i += 2
            continue

        if ch == "/" and nxt == "*":
            result.extend("  ")
            in_block = True
            i += 2
            continue

        if ch == '"':
            result.append(mask_char(ch))
            in_string = True
            quote = ch
            i += 1
            continue

        result.append(ch)
        i += 1

    return "".join(result)


def line_col(text: str, pos: int) -> tuple[int, int]:
    line = text.count("\n", 0, pos) + 1
    last_newline = text.rfind("\n", 0, pos)
    col = pos + 1 if last_newline == -1 else pos - last_newline
    return line, col


def location(base: Path, path: Path, pos: int, text: str) -> str:
    line, col = line_col(text, pos)
    try:
        rel = path.relative_to(base)
    except ValueError:
        rel = path
    return f"{rel}:{line}:{col}"


def search_release(name: str, patterns: tuple[re.Pattern[str], ...], text: str, start: int) -> bool:
    for pattern in patterns:
        if pattern.search(text, start):
            return True
        scoped = re.compile(rf"\b{re.escape(name)}{pattern.pattern}")
        if scoped.search(text, start):
            return True
    return False


def collect_issues(root: Path) -> list[tuple[str, str, str]]:
    issues: list[tuple[str, str, str]] = []
    base = root if root.is_dir() else root.parent

    for path in iter_swiftish_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        code = strip_comments_and_strings(text)
        seen: set[tuple[str, str, str]] = set()

        for kind, message, acquire, release_patterns in ASSIGNED_RULES:
            for match in acquire.finditer(code):
                name = match.group(1)
                if search_release(name, release_patterns, code, match.end()):
                    continue
                issue = (location(base, path, match.start(), text), kind, f"{message} ({name})")
                if issue not in seen:
                    seen.add(issue)
                    issues.append(issue)

        kvo_kind, kvo_message, kvo_acquire, kvo_release = KVO_RULE
        if not kvo_release.search(code):
            for match in kvo_acquire.finditer(code):
                issue = (location(base, path, match.start(), text), kvo_kind, kvo_message)
                if issue not in seen:
                    seen.add(issue)
                    issues.append(issue)

    return issues


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: resource_lifecycle_swift.py <project_dir>", file=sys.stderr)
        return 1
    root = Path(sys.argv[1]).resolve()
    if not root.exists():
        return 0
    for loc, kind, message in collect_issues(root):
        print(f"{loc}\t{kind}\t{message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
