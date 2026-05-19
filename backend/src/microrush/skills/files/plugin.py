"""File management plugin for Micro Rush."""

import os
from pathlib import Path
from typing import Optional, list
from ..plugins import Plugin


class FilePlugin(Plugin):
    """
    Smart file management — find, summarize, and organize documents.

    Capabilities:
    - Search files by name or content
    - Summarize document contents
    - Organize files by category
    - Full-text search across workspace
    """

    name = "files"
    description = "Smart file search and summarization"
    version = "0.1.0"

    def __init__(self, workspace_path: str = "/home/engine"):
        self.workspace_path = Path(workspace_path)

    def execute(self, context: dict) -> dict:
        """
        Handle file-related requests.

        Context keys:
        - action: "search" | "summarize" | "list_recent" | "find_by_content"
        - query: search term (for search/find_by_content)
        - path: specific path to process
        """
        action = context.get("action", "list_recent")
        query = context.get("query", "")

        if action == "search":
            return self._search_files(query)
        elif action == "summarize":
            return self._summarize_file(context.get("path", ""))
        elif action == "list_recent":
            return self._list_recent_files(context.get("limit", 10))
        elif action == "find_by_content":
            return self._find_by_content(query)
        else:
            return {"error": f"Unknown action: {action}"}

    def _search_files(self, query: str) -> dict:
        """Search files by name."""
        if not query:
            return {"error": "Query required for search"}

        results = []
        for path in self.workspace_path.rglob(f"*{query}*"):
            if path.is_file():
                results.append({
                    "name": path.name,
                    "path": str(path),
                    "size": path.stat().st_size,
                    "modified": path.stat().st_mtime,
                })
        return {"results": results[:20]}  # Limit to 20 results

    def _summarize_file(self, file_path: str) -> dict:
        """Get a summary of a file's contents."""
        path = Path(file_path)
        if not path.exists():
            return {"error": "File not found"}
        if not path.is_file():
            return {"error": "Not a file"}

        # Get file type and basic info
        suffix = path.suffix.lower()
        size = path.stat().st_size

        summary = {
            "name": path.name,
            "type": suffix or "unknown",
            "size": size,
            "path": str(path),
        }

        # For text files, get first few lines
        if suffix in {".txt", ".md", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml"}:
            try:
                with open(path) as f:
                    lines = [f.readline() for _ in range(10)]
                    summary["preview"] = "".join(lines)
                    summary["line_count"] = sum(1 for _ in open(path))
            except Exception:
                summary["preview"] = "[Binary file]"
        else:
            summary["preview"] = f"[{suffix} file - preview not available]"

        return summary

    def _list_recent_files(self, limit: int = 10) -> dict:
        """List most recently modified files."""
        if not self.workspace_path.exists():
            return {"error": "Workspace not found"}

        files = []
        try:
            for path in self.workspace_path.rglob("*"):
                if path.is_file():
                    files.append({
                        "name": path.name,
                        "path": str(path),
                        "modified": path.stat().st_mtime,
                    })
        except PermissionError:
            return {"error": "Permission denied"}

        recent = sorted(files, key=lambda f: f["modified"], reverse=True)[:limit]
        return {"results": recent}

    def _find_by_content(self, query: str) -> dict:
        """Find files containing a string (simple grep-like)."""
        if not query:
            return {"error": "Query required"}

        results = []
        try:
            for path in self.workspace_path.rglob("*"):
                if path.is_file() and path.stat().st_size < 1_000_000:  # Skip large files
                    try:
                        content = path.read_text(errors="ignore")
                        if query.lower() in content.lower():
                            results.append({
                                "name": path.name,
                                "path": str(path),
                                "match": True,
                            })
                    except:
                        pass
                    if len(results) >= 20:
                        break
        except PermissionError:
            return {"error": "Permission denied"}

        return {"results": results, "query": query}