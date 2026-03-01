# Project Tools

**Table of Contents**

- [Available Tools](#available-tools)
  - [rename_and_update_refs.py](#rename_and_update_refspy)
  - [find_broken_refs.py](#find_broken_refspy)
  - [md_toc.py](#md_tocpy)
- [rename_and_update_refs.py](#rename_and_update_refspy)
    - [Purpose](#purpose)
    - [Usage](#usage)
    - [Options](#options)
    - [How It Works](#how-it-works)
    - [Directory Support](#directory-support)
    - [File Type Support](#file-type-support)
    - [Best Practices](#best-practices)
    - [Examples](#examples)
    - [Troubleshooting](#troubleshooting)
    - [Limitations](#limitations)
    - [Technical Details](#technical-details)
- [find_broken_refs.py](#find_broken_refspy)
    - [Purpose](#purpose)
    - [Usage](#usage)
    - [Options](#options)
    - [How It Works](#how-it-works)
    - [Output Formats](#output-formats)
    - [File Type Support](#file-type-support)
    - [Best Practices](#best-practices)
    - [Examples](#examples)
    - [Known Limitations & False Positives](#known-limitations-false-positives)
    - [Filtering False Positives](#filtering-false-positives)
    - [Troubleshooting](#troubleshooting)
    - [Integration Ideas](#integration-ideas)
    - [Technical Details](#technical-details)
- [md_toc.py](#md_tocpy)
    - [Purpose](#purpose)
    - [Usage](#usage)
    - [Options](#options)
    - [How It Works](#how-it-works)
    - [Best Practices](#best-practices)
    - [Examples](#examples)
    - [Output Format](#output-format)
    - [Anchor Link Compatibility](#anchor-link-compatibility)
    - [Limitations](#limitations)
    - [Integration Ideas](#integration-ideas)
    - [Technical Details](#technical-details)
- [Contributing New Tools](#contributing-new-tools)


This directory contains utility scripts and tools to support project management and maintenance tasks.

## Available Tools

### rename_and_update_refs.py

A Python script that intelligently renames or moves files and directories while automatically updating all references throughout the workspace.

### find_broken_refs.py

A Python script that scans the workspace for broken references - links and textual references to files that don't exist.

### md_toc.py

A Python script that generates a table of contents for markdown files with navigatable links to chapters and sections.

---

## rename_and_update_refs.py

#### Purpose

When refactoring project structure or reorganizing documentation, manually updating all references to moved files is error-prone and time-consuming. This tool automates the entire process:

1. Renames/moves the file or directory
2. Searches all workspace files for references
3. Updates all found references to the new location

#### Usage

```bash
# Basic syntax
python3 project_management/00_tools/rename_and_update_refs.py <old_path> <new_path> [--dry-run]

# Rename a single file
python3 project_management/00_tools/rename_and_update_refs.py \
  project_documentation/old_file.md \
  project_documentation/new_file.md

# Move a file to different directory
python3 project_management/00_tools/rename_and_update_refs.py \
  README.md \
  project_documentation/03_user_guide/README.md

# Rename a directory (updates all nested file references)
python3 project_management/00_tools/rename_and_update_refs.py \
  old_docs/ \
  new_docs/

# Move a directory tree
python3 project_management/00_tools/rename_and_update_refs.py \
  temp_folder/ \
  project_management/02_project_vision/temp_folder/

# Always test with --dry-run first!
python3 project_management/00_tools/rename_and_update_refs.py \
  old_path \
  new_path \
  --dry-run
```

#### Options

| Option | Description |
|--------|-------------|
| `old_path` | Current path of the file or directory (required) |
| `new_path` | New path for the file or directory (required) |
| `--dry-run` | Preview changes without applying them (recommended for first run) |
| `--workspace PATH` | Specify workspace root directory (default: auto-detected) |

#### How It Works

**Step 1: Reference Discovery**
- Scans all searchable files in the workspace (`.md`, `.txt`, `.py`, `.json`, `.yaml`, etc.)
- Excludes common directories like `.git`, `node_modules`, `__pycache__`, build outputs
- Generates multiple search patterns for each target:
  - Full POSIX paths: `foo/bar/file.md`
  - Windows paths: `foo\bar\file.md`
  - Filename only: `file.md` (with word boundaries)

**Step 2: Pattern Matching**
- Finds references regardless of syntax:
  - Plain text: `./foo/bar/file.md`
  - Quoted: `'./foo/bar/file.md'` or `"./foo/bar/file.md"`
  - Backticks: `` `./foo/bar/file.md` ``
  - Markdown links: `[link](foo/bar/file.md)`
  - Any combination of the above

**Step 3: File/Directory Rename**
- Creates parent directories if needed
- Validates that destination doesn't already exist
- Performs atomic rename/move operation

**Step 4: Reference Updates**
- Replaces all found references with new paths
- Preserves surrounding syntax (quotes, backticks, etc.)
- Updates files in-place with UTF-8 encoding

**Step 5: Summary Report**
- Lists all modified files
- Counts total updates made
- Provides clear success/failure feedback

#### Directory Support

When renaming/moving directories, the tool:
- Recursively collects all files within the directory
- Builds a mapping of old paths → new paths for every file
- Updates references to both the directory itself and all nested files
- Example: Moving `docs/` to `documentation/` will update:
  - `docs/guide.md` → `documentation/guide.md`
  - `docs/api/reference.md` → `documentation/api/reference.md`
  - References to any file within the moved tree

#### File Type Support

The script searches these file types by default:

**Documentation**: `.md`, `.txt`, `.adoc`  

#### Best Practices

1. **Always use `--dry-run` first** to preview changes before applying them
2. **Commit your work** before running the tool so you can revert if needed
3. **Review the summary** to ensure expected files were updated
4. **Run from workspace root** for best results (auto-detection works from subdirectories too)
5. **Use relative paths** rather than absolute paths when possible
6. **Check excluded directories** if you expect files to be found but they're not being detected

#### Examples

**Example 1: Reorganizing documentation**
```bash
# Preview the move
python3 project_management/00_tools/rename_and_update_refs.py \
  project_documentation/guide.md \
  project_documentation/03_user_guide/guide.md \
  --dry-run

# Apply the move
python3 project_management/00_tools/rename_and_update_refs.py \
  project_documentation/guide.md \
  project_documentation/03_user_guide/guide.md
```

**Example 2: Renaming a requirements file**
```bash
python3 project_management/00_tools/rename_and_update_refs.py \
  project_management/02_project_vision/02_requirements/03_accepted/REQ-001.md \
  project_management/02_project_vision/02_requirements/03_accepted/REQ-AUTH-001.md
```

**Example 3: Moving an entire agent folder**
```bash
python3 project_management/00_tools/rename_and_update_refs.py \
  .github/old_agents/ \
  .github/agents/ \
  --dry-run
```

#### Troubleshooting

**Problem**: "Path not found" error  
**Solution**: Check that the old path exists and is spelled correctly. Paths are case-sensitive on Linux.

**Problem**: "Destination already exists" error  
**Solution**: Remove or rename the conflicting file/directory at the destination first.

**Problem**: Expected references weren't updated  
**Solution**: 
- Verify the file containing the reference has a searchable extension (see File Type Support)
- Check if the file is in an excluded directory (`.git`, `node_modules`, etc.)
- The reference might use an absolute path or different format than expected

**Problem**: Too many false positives in filename-only matching  
**Solution**: The script uses word boundaries to reduce false positives. If issues persist, references should use full paths rather than just filenames.

#### Limitations

- **Encoding**: Files must be UTF-8 compatible (uses `errors='ignore'` for robustness)
- **Line-based**: Assumes references don't span multiple lines
- **String replacement**: Uses literal string replacement, not semantic analysis
- **Symlinks**: Follows symlinks during search but doesn't update symlink targets
- **Git history**: Doesn't rewrite Git history (use `git filter-repo` for that)

#### Technical Details

**Language**: Python 3.7+  
**Dependencies**: Standard library only (no external packages required)  
**Entry point**: `rename_and_update_refs.py`  
**Key modules**: `pathlib`, `re`, `argparse`, `os`, `sys`

---

## find_broken_refs.py

A Python script that detects broken references throughout the workspace - identifying links and textual references to files that don't exist.

#### Purpose

Maintaining reference integrity across documentation and code is challenging in large projects. This tool scans the entire workspace to find references pointing to non-existent files, helping to:

1. Identify broken links in documentation
2. Detect outdated file references after restructuring
3. Validate documentation before releases
4. Find references in code comments pointing to missing files

#### Usage

```bash
# Basic scan
python3 project_management/00_tools/find_broken_refs.py

# Show verbose output with resolved paths
python3 project_management/00_tools/find_broken_refs.py --verbose

# Scan a specific workspace
python3 project_management/00_tools/find_broken_refs.py --workspace /path/to/project

# Simple output format (one line per finding)
python3 project_management/00_tools/find_broken_refs.py --format simple

# JSON output format (one JSON object per line)
python3 project_management/00_tools/find_broken_refs.py --format json
```

#### Options

| Option | Description |
|--------|-------------|
| `--workspace PATH` | Specify workspace root directory (default: auto-detected) |
| `--verbose`, `-v` | Show detailed output including how paths were resolved (only for full format) |
| `--format {full,simple,json}` | Output format: `full` (default, human-readable), `simple` (concise), `json` (JSON lines) |

#### How It Works

**Step 1: File Discovery**
- Scans all searchable files in the workspace (`.md`, `.txt`, `.py`, `.json`, etc.)
- Excludes common directories like `.git`, `node_modules`, build outputs
- Reports total number of files to search

**Step 2: Reference Extraction**
- Parses each file line-by-line to extract potential file references
- Detects multiple reference formats:
  - **Markdown links**: `[text](path/to/file.md)`
  - **Quoted paths**: `"path/to/file.txt"` or `'path/to/file.txt'`
  - **Backtick paths**: `` `path/to/config.yaml` ``
  - **Plain paths**: `path/to/file.py` (with file extension)

**Step 3: Path Resolution**
- Tries multiple resolution strategies for each reference:
  1. Relative to the source file's directory
  2. Relative to workspace root
  3. As absolute path (if provided)
- Uses the first candidate that exists

**Step 4: Existence Check**
- Verifies whether the resolved path exists on the filesystem
- Records references that point to non-existent files

**Step 5: Results Report**
- Groups broken references by source file
- Shows line number, reference type, and referenced path
- Provides summary statistics by reference type
- Returns exit code 1 if broken references found (useful for CI/CD)

#### Output Formats

The tool supports three output formats via the `--format` option:

**Full format** (default, `--format full`):
```
=== Broken References ===

test.md
───────
  Line    4 [markdown_link ]: docs/missing.md
  Line    5 [quoted_path   ]: path/to/missing.txt
  Line    6 [backtick_path ]: config/missing.yaml

════════════════════════════════════════════════════════════
Summary: 3 broken reference(s) in 1 file(s)
════════════════════════════════════════════════════════════
```

**Simple format** (`--format simple`):
One line per finding: `<file> <tangledRef>`
```
test.md docs/missing.md
test.md path/to/missing.txt
test.md config/missing.yaml
```
Best for: scripting, piping to other tools, concise output

**JSON format** (`--format json`):
One JSON object per line (JSON Lines format):
```json
{"file": "test.md", "tangledRef": "docs/missing.md", "line": 4, "type": "markdown_link"}
{"file": "test.md", "tangledRef": "path/to/missing.txt", "line": 5, "type": "quoted_path"}
{"file": "test.md", "tangledRef": "config/missing.yaml", "line": 6, "type": "backtick_path"}
```
Best for: parsing with `jq`, programmatic processing, detailed analysis

**Verbose mode** (only with full format):
Add `--verbose` to show path resolution details:
```
test.md
───────
  Line    4 [markdown_link ]: docs/missing.md
              → Resolved to: /full/path/to/docs/missing.md
              → File does not exist
```

#### File Type Support

The script searches these file types by default:

**Documentation**: `.md`, `.txt`, `.rst`, `.adoc`  
**Code**: `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.c`, `.h`  
**Config**: `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`  
**Web**: `.html`, `.xml`, `.css`, `.scss`  
**Shell**: `.sh`, `.bash`, `.zsh`

#### Best Practices

1. **Run regularly** during development to catch broken references early
2. **Use in CI/CD** to prevent merging broken documentation
3. **Review false positives** - URLs and example paths will be flagged
4. **Use `--verbose`** when debugging specific reference issues
5. **Run after restructuring** to ensure all references were updated
6. **Filter results** if needed using standard Unix tools (grep, awk)

#### Examples

**Example 1: Quick workspace scan**
```bash
python3 project_management/00_tools/find_broken_refs.py
```

**Example 2: Detailed troubleshooting**
```bash
python3 project_management/00_tools/find_broken_refs.py --verbose
```

**Example 3: Simple output for scripting**
```bash
# Get simple list of broken references
python3 project_management/00_tools/find_broken_refs.py --format simple

# Count broken references per file
python3 project_management/00_tools/find_broken_refs.py --format simple | cut -d' ' -f1 | sort | uniq -c

# Find all broken markdown files
python3 project_management/00_tools/find_broken_refs.py --format simple | grep '\.md$'
```

**Example 4: JSON output for programmatic processing**
```bash
# Get JSON output
python3 project_management/00_tools/find_broken_refs.py --format json

# Use jq to filter markdown links only
python3 project_management/00_tools/find_broken_refs.py --format json | jq 'select(.type == "markdown_link")'

# Count by reference type
python3 project_management/00_tools/find_broken_refs.py --format json | jq -r '.type' | sort | uniq -c
```

**Example 5: CI/CD integration**
```bash
# In your CI pipeline
python3 project_management/00_tools/find_broken_refs.py
# Script exits with code 1 if broken refs found, failing the build
```

**Example 6: Filter specific files**
```bash
# Only show .md files with broken refs (simple format)
python3 project_management/00_tools/find_broken_refs.py --format simple | grep '^.*\.md '
```

#### Known Limitations & False Positives

**False Positives** (will be flagged as broken):
- **URLs**: `github.com/user/repo` or `example.com/path`
  - URLs match the path pattern but don't exist as local files
- **Example paths**: Documentation showing path examples
- **JSON keys**: Config keys like `editor.formatOnSave` with dots
- **Generated files**: References to files created at build time

**Actual Limitations**:
- **Encoding**: Requires UTF-8 compatible files (uses `errors='ignore'`)
- **Line-based parsing**: References spanning multiple lines won't be detected
- **Anchor links**: `file.md#section` - anchors are stripped before validation
- **External references**: Only checks workspace-relative paths
- **Case sensitivity**: Path matching is case-sensitive on Linux
- **Symlinks**: Doesn't validate symlink targets

#### Filtering False Positives

The tool reports everything it finds to ensure no real broken references are missed. You can filter results using standard tools:

**With full format:**
```bash
# Exclude URLs (containing .com, .org, etc.)
python3 project_management/00_tools/find_broken_refs.py | grep -v "\.com\|\.org"

# Only show markdown files with issues
python3 project_management/00_tools/find_broken_refs.py | grep "\.md$" -A 10

# Count broken refs per file
python3 project_management/00_tools/find_broken_refs.py | grep "^[^ ]" | wc -l
```

**With simple format (easier filtering):**
```bash
# Exclude URLs
python3 project_management/00_tools/find_broken_refs.py --format simple | grep -v "\.com\|\.org"

# Only markdown files
python3 project_management/00_tools/find_broken_refs.py --format simple | grep '\.md '

# Group by file
python3 project_management/00_tools/find_broken_refs.py --format simple | cut -d' ' -f1 | sort | uniq -c
```

**With JSON format (most flexible):**
```bash
# Filter by type using jq
python3 project_management/00_tools/find_broken_refs.py --format json | jq 'select(.type == "markdown_link")'

# Exclude specific patterns
python3 project_management/00_tools/find_broken_refs.py --format json | jq 'select(.tangledRef | test("\\.com|\\.org") | not)'

# Get unique files with issues
python3 project_management/00_tools/find_broken_refs.py --format json | jq -r '.file' | sort -u
```

#### Troubleshooting

**Problem**: High number of false positives  
**Solution**: 
- URLs and example paths in documentation are expected
- Use grep to filter known patterns
- Review the context - broken refs in TOOLS.md examples are usually intentional

**Problem**: Missing expected broken references  
**Solution**:
- Check that the source file has a searchable extension
- Verify the file isn't in an excluded directory
- Try `--verbose` to see how paths are being resolved
- Ensure the reference has a file extension (required for plain path detection)

**Problem**: "File does not exist" but the file exists  
**Solution**:
- Path might be using the wrong case (Linux is case-sensitive)
- Reference might use `\` on Linux (should use `/`)
- File might be outside the workspace
- Use `--verbose` to see the resolved path

#### Integration Ideas

**Pre-commit hook:**
```bash
#!/bin/bash
python3 project_management/00_tools/find_broken_refs.py
if [ $? -ne 0 ]; then
    echo "Fix broken references before committing"
    exit 1
fi
```

**GitHub Actions:**
```yaml
- name: Check for broken references
  run: |
    python3 project_management/00_tools/find_broken_refs.py
    if [ $? -eq 1 ]; then
      echo "::error::Broken references detected"
      exit 1
    fi
```

#### Technical Details

**Language**: Python 3.7+  
**Dependencies**: Standard library only (no external packages required)  
**Entry point**: `find_broken_refs.py`  
**Key modules**: `pathlib`, `re`, `argparse`, `os`, `sys`, `collections`  
**Exit codes**: 0 = no broken refs, 1 = broken refs found

---

## md_toc.py

A Python script that generates a table of contents for markdown files by extracting heading elements and creating navigatable links.

#### Purpose

Maintaining a table of contents in markdown documentation improves readability and navigation, especially in long documents. This tool automates TOC generation:

1. Extracts all markdown headings from a file
2. Generates GitHub-compatible anchor links
3. Creates hierarchical structure with proper indentation
4. Can insert TOC directly into the file or output separately
5. Automatically replaces existing TOC when updating

#### Usage

```bash
# Print TOC to stdout
python3 project_management/00_tools/md_toc.py file.md

# Insert TOC into the file after the first heading
python3 project_management/00_tools/md_toc.py file.md --insert

# Update existing TOC (or insert if not present)
python3 project_management/00_tools/md_toc.py file.md --update

# Save TOC to a separate file
python3 project_management/00_tools/md_toc.py file.md --output toc.md

# Filter heading levels (e.g., only h2 through h4)
python3 project_management/00_tools/md_toc.py file.md --min-level 2 --max-level 4

# Update TOC with filtered levels
python3 project_management/00_tools/md_toc.py file.md --update --min-level 2 --max-level 3
```

#### Options

| Option | Description |
|--------|-------------|
| `file` | Markdown file to process (required) |
| `--insert` | Insert TOC into the file after the first heading |
| `--update` | Update existing TOC or insert if not present (same as --insert) |
| `--output FILE`, `-o FILE` | Write TOC to specific file |
| `--max-level N` | Maximum heading level to include (default: 6) |
| `--min-level N` | Minimum heading level to include (default: 1) |

#### How It Works

**Step 1: Heading Extraction**
- Parses markdown file line-by-line
- Detects ATX-style headings (`#` through `######`)
- Extracts heading level and text
- Filters headings based on `--min-level` and `--max-level` options

**Step 2: Link Generation**
- Converts heading text to GitHub-compatible anchor links
- Removes markdown formatting (bold, italic, code, links)
- Converts to lowercase and replaces spaces with hyphens
- Strips special characters to create URL-safe anchors

**Step 3: TOC Structure**
- Calculates proper indentation based on heading hierarchy
- Creates markdown list with navigatable links
  ```markdown
  **Table of Contents**
  
  - [Chapter 1](#chapter-1)
    - [Section 1.1](#section-11)
    - [Section 1.2](#section-12)
  - [Chapter 2](#chapter-2)
  ```

**Step 4: Output Handling**
- **Default**: Prints TOC to stdout
- **`--insert`**: Replaces existing TOC (if found) and inserts after first heading
- **`--output`**: Writes TOC to specified file

#### Best Practices

1. **Generate regularly** after adding new sections to documentation
2. **Use `--insert`** to maintain TOC in the document itself
3. **Filter levels** to avoid overly detailed TOCs in long documents
4. **Commit TOC updates** along with content changes
5. **Preview first** by running without `--insert`/`--update` to see the output
6. **Use `--update`** for clarity when refreshing existing TOCs (reports "updated" vs "inserted")

#### Examples

**Example 1: Generate TOC for README**
```bash
python3 project_management/00_tools/md_toc.py README.md
```

**Example 2: Insert TOC into architecture document**
```bash
python3 project_management/00_tools/md_toc.py \
  project_documentation/01_architecture/01_introduction_and_goals/introduction.md \
  --insert
```

**Example 3: Update existing TOC after adding new sections**
```bash
python3 project_management/00_tools/md_toc.py guide.md --update --min-level 2
```

**Example 4: Create TOC with only main sections (h2 and h3)**
```bash
python3 project_management/00_tools/md_toc.py guide.md \
  --min-level 2 \
  --max-level 3 \
  --insert
```

**Example 5: Save TOC to separate file**
```bash
python3 project_management/00_tools/md_toc.py documentation.md \
  --output table_of_contents.md
```

**Example 6: Batch update all requirements files**
```bash
for file in project_management/02_project_vision/02_requirements/03_accepted/*.md; do
  python3 project_management/00_tools/md_toc.py "$file" --update --min-level 2
done
```

#### Output Format

The generated TOC follows this structure:

```markdown
**Table of Contents**

- [First Level Heading](#first-level-heading)
  - [Second Level Heading](#second-level-heading)
    - [Third Level Heading](#third-level-heading)
```

**Key features:**
- Bold title "**Table of Contents**"
- Blank line after title
- Hierarchical bullets with 2-space indentation per level
- GitHub-compatible anchor links
- Blank line after TOC for separation

#### Anchor Link Compatibility

The script generates anchor links compatible with GitHub's markdown rendering:

- Converts to lowercase
- Replaces spaces with hyphens
- Removes special characters
- Strips markdown formatting from heading text
- Example: `## API Reference (v2.0)` → `#api-reference-v20`

#### Limitations

- **ATX-style only**: Supports `#` headings, not underline-style (`===` or `---`)
- **Single-line headings**: Headings must be on a single line
- **No Setext headings**: Underlined headings are not detected
- **GitHub anchors**: Anchor format follows GitHub conventions (may differ on other platforms)
- **ASCII-friendly**: Non-ASCII characters in headings may create different anchors than expected

#### Integration Ideas

**Pre-commit hook for documentation:**
```bash
#!/bin/bash
# Auto-update TOC in all markdown files with TOC section
for file in $(git diff --cached --name-only | grep '\.md$'); do
  if grep -q "Table of Contents" "$file"; then
    python3 project_management/00_tools/md_toc.py "$file" --update
    git add "$file"
  fi
done
```

**Makefile target:**
```makefile
.PHONY: toc
toc:
	@echo "Updating table of contents..."
	@python3 project_management/00_tools/md_toc.py README.md --update
	@echo "TOC updated successfully"
```

**VS Code task:**
```json
{
  "label": "Update TOC",
  "type": "shell",
  "command": "python3 project_management/00_tools/md_toc.py ${file} --update"
}
```

#### Technical Details

**Language**: Python 3.7+  
**Dependencies**: Standard library only (no external packages required)  
**Entry point**: `md_toc.py`  
**Key modules**: `re`, `argparse`, `pathlib`, `sys`  
**Encoding**: UTF-8

---

## Contributing New Tools

When adding new tools to this directory:

1. Create the tool script with a descriptive name
2. Add execution permissions: `chmod +x tool_name.py`
3. Include comprehensive `--help` documentation
4. Update this `TOOLS.md` file with tool documentation
5. Follow the documentation template structure shown above
6. Add usage examples relevant to project workflows
