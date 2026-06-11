#!/usr/bin/env python3
import os
import sys
import re
import fnmatch
import argparse
from datetime import datetime

# Default directories and files to ignore
DEFAULT_IGNORES = {
    # System and IDE
    '.git', '.vscode', '.idea', '.DS_Store', 'Thumbs.db', '.gemini',
    # Python
    '__pycache__', '.pytest_cache', '.ruff_cache', '.venv', 'venv', 'env',
    # JS / Web
    'node_modules', 'dist', 'build', '.next', '.nuxt',
}

# Files that should always be excluded from output
SELF_EXCLUDES = {'analyze.py', 'codebase_summary.md'}

# Mapping of file extensions to markdown language tags for syntax highlighting
LANGUAGE_TAGS = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.json': 'json',
    '.md': 'markdown',
    '.html': 'html',
    '.css': 'css',
    '.sh': 'bash',
    '.bash': 'bash',
    '.ps1': 'powershell',
    '.rs': 'rust',
    '.go': 'go',
    '.c': 'c',
    '.cpp': 'cpp',
    '.h': 'cpp',
    '.hpp': 'cpp',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.toml': 'toml',
    '.xml': 'xml',
    '.sql': 'sql',
    '.ini': 'ini',
    '.conf': 'ini',
    '.dockerfile': 'dockerfile',
    'Dockerfile': 'dockerfile',
}


def parse_gitignore_line(line, base_dir):
    """
    Parses a single .gitignore line and returns a tuple (compiled_regex, negate) or None.
    base_dir is the absolute path of the directory containing the .gitignore file.
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None

    negate = False
    if line.startswith('!'):
        negate = True
        line = line[1:]

    # Normalize Windows path separators
    line = line.replace('\\', '/')

    match_dir_only = False
    if line.endswith('/'):
        match_dir_only = True
        line = line[:-1]

    # Convert gitignore pattern to regex
    parts = []
    i = 0
    n = len(line)
    is_anchored = '/' in line or line.startswith('/')

    if line.startswith('/'):
        line = line[1:]

    while i < n:
        char = line[i]
        if char == '*':
            if i + 1 < n and line[i+1] == '*':
                if i + 2 < n and line[i+2] == '/':
                    parts.append('(?:.*/)?')
                    i += 3
                else:
                    parts.append('.*')
                    i += 2
            else:
                parts.append('[^/]*')
                i += 1
        elif char == '?':
            parts.append('[^/]')
            i += 1
        elif char in ['.', '+', '^', '$', '(', ')', '[', ']', '{', '}', '|']:
            parts.append(re.escape(char))
            i += 1
        else:
            parts.append(char)
            i += 1

    regex_str = ''.join(parts)

    if not is_anchored:
        regex_str = f'(?:^|.*/){regex_str}'
    else:
        regex_str = f'^{regex_str}'

    if match_dir_only:
        regex_str = f'{regex_str}/(?:$|.*)'
    else:
        regex_str = f'{regex_str}(?:$|/.*)'

    try:
        compiled = re.compile(regex_str)
        return compiled, negate
    except Exception:
        return None


class GitIgnoreMatcher:
    """Manages loading and matching of .gitignore files down a directory tree."""
    def __init__(self, root_dir, use_defaults=True):
        self.root_dir = os.path.abspath(root_dir)
        self.use_defaults = use_defaults
        # Map directory path -> list of (regex, negate)
        self.rules_cache = {}

    def load_for_dir(self, dir_path):
        dir_path = os.path.abspath(dir_path)
        if dir_path in self.rules_cache:
            return self.rules_cache[dir_path]

        rules = []
        gitignore_path = os.path.join(dir_path, '.gitignore')
        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        rule = parse_gitignore_line(line, dir_path)
                        if rule:
                            rules.append(rule)
            except Exception as e:
                print(f"Warning: Failed to read {gitignore_path}: {e}", file=sys.stderr)

        self.rules_cache[dir_path] = rules
        return rules

    def is_ignored(self, path, is_dir=False):
        abs_path = os.path.abspath(path)

        # Check default system ignores first if enabled
        if self.use_defaults:
            rel_parts = os.path.relpath(abs_path, self.root_dir).replace('\\', '/').split('/')
            for part in rel_parts:
                if part in DEFAULT_IGNORES:
                    return True

        # Resolve all ancestor directories up to the root_dir
        ancestors = []
        curr = abs_path if is_dir else os.path.dirname(abs_path)

        while True:
            ancestors.append(curr)
            if curr == self.root_dir or curr == os.path.dirname(curr):
                break
            curr = os.path.dirname(curr)

        # Apply rules starting from root_dir down to the file's dir
        ancestors.reverse()
        ignored = False

        for ancestor in ancestors:
            if not ancestor.startswith(self.root_dir):
                continue
            rules = self.load_for_dir(ancestor)
            rel_path = os.path.relpath(abs_path, ancestor).replace('\\', '/')
            if is_dir and not rel_path.endswith('/'):
                rel_path += '/'

            for regex, negate in rules:
                if regex.match(rel_path):
                    ignored = not negate

        return ignored


def is_binary(file_path):
    """Detects if a file is binary by looking for a null byte in the first 1024 bytes."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except Exception:
        # Treat files we can't open as binary / unreadable
        return True


def matches_any_pattern(rel_path, patterns, is_dir=False):
    """Checks if a relative path matches any custom glob pattern."""
    for pat in patterns:
        pat = pat.strip()
        if not pat:
            continue

        pat = pat.replace('\\', '/')

        # Handle directory-only patterns (ending with /)
        if pat.endswith('/'):
            if not is_dir:
                continue
            pat_clean = pat[:-1]
        else:
            pat_clean = pat

        name = rel_path.split('/')[-1]

        # If pattern contains slashes, match against relative path. Otherwise match name.
        if '/' in pat_clean:
            if fnmatch.fnmatch(rel_path, pat_clean) or fnmatch.fnmatch(rel_path + ('/' if is_dir else ''), pat_clean):
                return True
        else:
            if fnmatch.fnmatch(name, pat_clean):
                return True
    return False


def get_code_fence(content):
    """Calculates the markdown code fence backtick count to prevent nested block breaks."""
    max_backticks = 0
    curr_backticks = 0
    for char in content:
        if char == '`':
            curr_backticks += 1
            if curr_backticks > max_backticks:
                max_backticks = curr_backticks
        else:
            curr_backticks = 0
    fence_len = max(3, max_backticks + 1)
    return '`' * fence_len


def build_ascii_tree(dir_path, matcher, custom_excludes=None, prefix="", root_dir=None, output_path=None):
    """Generates a list of strings representing the ASCII tree structure of the directory."""
    if root_dir is None:
        root_dir = dir_path

    lines = []
    try:
        entries = sorted(os.listdir(dir_path))
    except Exception as e:
        return [f"{prefix}└── [Error reading directory: {e}]"]

    filtered = []
    for entry in entries:
        full_path = os.path.join(dir_path, entry)
        is_dir = os.path.isdir(full_path)
        rel_path = os.path.relpath(full_path, root_dir).replace('\\', '/')

        # Skip the output file itself
        if output_path and os.path.normcase(os.path.abspath(full_path)) == os.path.normcase(os.path.abspath(output_path)):
            continue

        # Apply ignores
        if matcher.is_ignored(full_path, is_dir=is_dir):
            continue
        if custom_excludes and matches_any_pattern(rel_path, custom_excludes, is_dir=is_dir):
            continue

        filtered.append((entry, full_path, is_dir))

    for index, (entry, full_path, is_dir) in enumerate(filtered):
        is_last = (index == len(filtered) - 1)
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{entry}{'/' if is_dir else ''}")

        if is_dir:
            sub_prefix = "    " if is_last else "│   "
            lines.extend(build_ascii_tree(full_path, matcher, custom_excludes, prefix + sub_prefix, root_dir, output_path))

    return lines


def parse_existing_summary(output_path):
    """
    Parses an existing summary file and returns a dict mapping relative path
    to a dictionary containing:
      - 'mtime': float
      - 'tokens': int
      - 'section_text': str
    """
    cache = {}
    if not os.path.exists(output_path):
        return cache

    try:
        with open(output_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except Exception:
        return cache

    # Find all file section starts: e.g., "### File: `path`" at the beginning of a line
    pattern = re.compile(r'^### File: `([^`]+)`', re.MULTILINE)
    matches = list(pattern.finditer(text))

    for idx, match in enumerate(matches):
        rel_path = match.group(1)
        start_pos = match.start()

        if idx + 1 < len(matches):
            end_pos = matches[idx + 1].start()
        else:
            end_pos = len(text)

        section_text = text[start_pos:end_pos].strip()

        # Remove trailing separator if present
        if section_text.endswith('---'):
            section_text = section_text[:-3].strip()

        # Parse mtime from this section_text
        mtime_match = re.search(r'-\s+\*\*mtime:\*\*\s+([\d.]+)', section_text)
        tokens_match = re.search(r'-\s+\*\*Estimated Tokens:\*\*\s+([\d,]+)', section_text)

        if mtime_match:
            try:
                mtime_val = float(mtime_match.group(1))
            except ValueError:
                mtime_val = 0.0

            tokens_val = 0
            if tokens_match:
                try:
                    tokens_val = int(tokens_match.group(1).replace(',', ''))
                except ValueError:
                    pass

            cache[rel_path] = {
                'mtime': mtime_val,
                'tokens': tokens_val,
                'section_text': section_text
            }

    return cache


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a folder end-to-end and generate a single Markdown summary for LLM context windows."
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="The target directory to scan (default: current directory)."
    )
    parser.add_argument(
        "-o", "--output",
        default="codebase_summary.md",
        help="Path to write the markdown summary file (default: codebase_summary.md)."
    )
    parser.add_argument(
        "-e", "--exclude",
        help="Comma-separated list of additional glob patterns to exclude (e.g. '*.log,tests/')."
    )
    parser.add_argument(
        "-t", "--token-limit",
        type=int,
        default=200000,
        help="Estimated token limit warning threshold (default: 200,000)."
    )
    parser.add_argument(
        "--no-defaults",
        action="store_true",
        help="Disable default ignore patterns (system and IDE directories, caches, etc.)."
    )
    parser.add_argument(
        "-y", "--non-interactive",
        action="store_true",
        help="Skip all confirmation prompts (for automated/agent usage)."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if the summary is fresh. Exit 0 if up-to-date, exit 1 if stale/missing."
    )
    parser.add_argument(
        "--max-file-tokens",
        type=int,
        default=0,
        help="Skip files exceeding this token estimate (0 = no limit). Recommended: 5000 for agent use."
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Output only tree + file metadata (path, tokens, lines) without code blocks. Ultra-compact mode."
    )
    args = parser.parse_args()

    target_dir = os.path.abspath(args.target_dir)
    output_path = os.path.abspath(args.output)
    custom_excludes = [p.strip() for p in args.exclude.split(',')] if args.exclude else []

    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning target directory: {target_dir}")
    print(f"Output markdown path:      {output_path}")

    # Load existing summary cache if available
    print("Loading existing summary cache...")
    cache = parse_existing_summary(output_path)
    if cache:
        print(f"Loaded {len(cache)} files from cache.")

    # --check mode: quick staleness test without regenerating
    if args.check:
        if not cache:
            print("CHECK: Summary missing or unparseable. Stale.")
            sys.exit(1)
        # Quick walk to compare mtimes
        stale = False
        temp_matcher = GitIgnoreMatcher(target_dir, use_defaults=not args.no_defaults)
        current_files = set()
        for root, dirs, filenames in os.walk(target_dir):
            pruned = []
            for d in dirs:
                dp = os.path.join(root, d)
                if temp_matcher.is_ignored(dp, is_dir=True):
                    continue
                if custom_excludes and matches_any_pattern(os.path.relpath(dp, target_dir).replace('\\', '/'), custom_excludes, is_dir=True):
                    continue
                pruned.append(d)
            dirs[:] = pruned
            for f in filenames:
                fp = os.path.join(root, f)
                rp = os.path.relpath(fp, target_dir).replace('\\', '/')
                if os.path.normcase(os.path.abspath(fp)) == os.path.normcase(output_path):
                    continue
                if temp_matcher.is_ignored(fp, is_dir=False):
                    continue
                if os.path.basename(fp) in SELF_EXCLUDES:
                    continue
                if is_binary(fp):
                    continue
                current_files.add(rp)
                try:
                    mtime = round(os.path.getmtime(fp), 3)
                except Exception:
                    mtime = 0.0
                if rp not in cache or abs(cache[rp]['mtime'] - mtime) >= 0.001:
                    stale = True
                    break
            if stale:
                break
        # Check for deleted files
        if not stale and set(cache.keys()) != current_files:
            stale = True
        if stale:
            print("CHECK: Summary is STALE. Regeneration needed.")
            sys.exit(1)
        else:
            print("CHECK: Summary is FRESH. No changes detected.")
            sys.exit(0)

    # Setup matcher
    matcher = GitIgnoreMatcher(target_dir, use_defaults=not args.no_defaults)

    # Gather files
    files_to_process = []
    file_status = {}
    total_chars = 0
    total_estimated_tokens = 0
    cache_hits = 0
    cache_misses = 0

    for root, dirs, filenames in os.walk(target_dir):
        # Exclude directories in-place to prevent os.walk from entering them
        pruned_dirs = []
        for d in dirs:
            dir_path = os.path.join(root, d)
            rel_dir_path = os.path.relpath(dir_path, target_dir).replace('\\', '/')
            if matcher.is_ignored(dir_path, is_dir=True):
                continue
            if custom_excludes and matches_any_pattern(rel_dir_path, custom_excludes, is_dir=True):
                continue
            pruned_dirs.append(d)
        dirs[:] = pruned_dirs  # Modifying in-place prunes walk recursion

        for f in filenames:
            file_path = os.path.join(root, f)
            rel_file_path = os.path.relpath(file_path, target_dir).replace('\\', '/')

            # Skip the output file itself
            if os.path.normcase(os.path.abspath(file_path)) == os.path.normcase(output_path):
                continue

            if matcher.is_ignored(file_path, is_dir=False):
                continue
            if custom_excludes and matches_any_pattern(rel_file_path, custom_excludes, is_dir=False):
                continue

            # Skip the script itself and its output
            if os.path.basename(file_path) in SELF_EXCLUDES:
                continue

            # Check if binary
            if is_binary(file_path):
                continue

            # Check mtime cache
            try:
                mtime = round(os.path.getmtime(file_path), 3)
            except Exception:
                mtime = 0.0

            is_cached = False
            if rel_file_path in cache:
                cached_info = cache[rel_file_path]
                if abs(cached_info['mtime'] - mtime) < 0.001:
                    is_cached = True

            if is_cached:
                cache_hits += 1
                file_status[rel_file_path] = {
                    'status': 'cached',
                    'mtime': mtime,
                    'tokens': cache[rel_file_path]['tokens'],
                    'section_text': cache[rel_file_path]['section_text']
                }
                total_estimated_tokens += cache[rel_file_path]['tokens']
            else:
                cache_misses += 1
                try:
                    file_size = os.path.getsize(file_path)
                except Exception:
                    file_size = 0
                file_est_tokens = file_size // 4

                # Skip files exceeding max-file-tokens threshold
                if args.max_file_tokens > 0 and file_est_tokens > args.max_file_tokens:
                    print(f"  Skipping {rel_file_path} (~{file_est_tokens:,} tokens > limit {args.max_file_tokens:,})")
                    continue

                file_status[rel_file_path] = {
                    'status': 'dirty',
                    'mtime': mtime,
                    'abs_path': file_path
                }
                total_chars += file_size

            files_to_process.append(rel_file_path)

    # Sort files for deterministic layout
    files_to_process.sort()

    total_estimated_tokens += total_chars // 4
    print(f"Found {len(files_to_process)} text files.")
    print(f"  - {cache_hits} files up-to-date (using cache)")
    print(f"  - {cache_misses} files modified/new (will be processed)")
    print(f"Estimated total size: ~{total_estimated_tokens:,} tokens.")

    if total_estimated_tokens > args.token_limit:
        print(f"\nWARNING: Estimated token count ({total_estimated_tokens:,}) exceeds the threshold ({args.token_limit:,}).")
        if not args.non_interactive:
            confirm = input("Do you want to continue? [y/N]: ").strip().lower()
            if confirm not in ('y', 'yes'):
                print("Aborted.")
                sys.exit(0)
        else:
            print("Non-interactive mode: proceeding anyway.")

    # Generate the tree structure
    print("Generating directory tree...")
    tree_lines = build_ascii_tree(target_dir, matcher, custom_excludes, output_path=output_path)
    tree_text = "\n".join(tree_lines)

    # Start writing output file
    print("Writing summary report...")
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            # Metadata header
            out.write(f"# Codebase Summary: {os.path.basename(target_dir)}\n\n")
            out.write("## Overview\n")
            out.write(f"- **Scan Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out.write(f"- **Source Folder:** `{target_dir}`\n")
            out.write(f"- **Total Text Files:** {len(files_to_process)}\n")
            out.write(f"- **Estimated Token Count:** {total_estimated_tokens:,}\n\n")

            # ASCII Tree
            out.write("## Directory Tree\n")
            out.write("```text\n")
            out.write(f"{os.path.basename(target_dir)}/\n")
            out.write(tree_text)
            out.write("\n```\n\n")

            # Files Content
            out.write("## File Contents\n\n")

            for idx, rel_path in enumerate(files_to_process, 1):
                status_info = file_status[rel_path]

                if args.summary_only:
                    # Ultra-compact: metadata only, no code blocks
                    print(f"[{idx}/{len(files_to_process)}] {rel_path} (metadata only)...")
                    if status_info['status'] == 'cached':
                        tokens = status_info['tokens']
                    else:
                        abs_path = status_info['abs_path']
                        try:
                            tokens = os.path.getsize(abs_path) // 4
                            line_count = sum(1 for _ in open(abs_path, 'r', encoding='utf-8', errors='replace'))
                        except Exception:
                            tokens = 0
                            line_count = 0
                    out.write(f"- `{rel_path}` — ~{tokens:,} tokens")
                    if status_info['status'] != 'cached':
                        out.write(f", {line_count} lines")
                    out.write("\n")

                elif status_info['status'] == 'cached':
                    print(f"[{idx}/{len(files_to_process)}] Processing {rel_path} (cached)...")
                    out.write(status_info['section_text'])
                    out.write("\n\n---\n\n")

                else:
                    print(f"[{idx}/{len(files_to_process)}] Processing {rel_path}...")
                    abs_path = status_info['abs_path']
                    try:
                        with open(abs_path, 'r', encoding='utf-8', errors='replace') as f_in:
                            content = f_in.read()
                    except Exception as e:
                        content = f"[Error reading file: {e}]"

                    file_ext = os.path.splitext(rel_path)[1]
                    lang_tag = LANGUAGE_TAGS.get(file_ext, LANGUAGE_TAGS.get(os.path.basename(rel_path), ''))

                    fence = get_code_fence(content)
                    file_tokens = len(content) // 4
                    mtime = status_info['mtime']

                    out.write(f"### File: `{rel_path}`\n")
                    out.write(f"- **Path:** `{rel_path}`\n")
                    out.write(f"- **Estimated Tokens:** {file_tokens:,}\n")
                    out.write(f"- **mtime:** {mtime}\n\n")
                    out.write(f"{fence}{lang_tag}\n")
                    out.write(content)
                    if not content.endswith('\n'):
                        out.write('\n')
                    out.write(f"{fence}\n\n")
                    out.write("---\n\n")

        print(f"\nSuccess! Codebase summary saved to: {output_path}")

    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
