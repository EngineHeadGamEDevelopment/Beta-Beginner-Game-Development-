"""
Draegtile Data Handler
========================
Handles real-time data fetching and pre-processing.

Inspired by:
  - guides/A basic python idea script module for complete implementation.txt (DataHandler)
  - guides/Python Detailer.txt (RealTimeDataReader)
  - guides/Basic weather and news AI models using python script.txt
"""

import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional


class DataHandler:
    """
    Fetches data from one or more URL sources and provides basic
    pre-processing helpers.  Uses only the Python standard library so that
    no third-party packages are required.
    """

    def __init__(self, sources: Optional[List[str]] = None) -> None:
        self.sources: List[str] = sources or []
        self._cache: Dict[str, Any] = {}

    def add_source(self, url: str) -> None:
        """Register a new data source URL."""
        if url not in self.sources:
            self.sources.append(url)

    def fetch(self, url: str, timeout: int = 10) -> Optional[Any]:
        """
        Fetch JSON data from *url*.  Returns the parsed object or None on
        error.  Result is cached in ``self._cache``.
        """
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                self._cache[url] = data
                return data
        except urllib.error.URLError as exc:
            print(f"[DataHandler] Network error fetching {url}: {exc}")
        except json.JSONDecodeError as exc:
            print(f"[DataHandler] JSON decode error for {url}: {exc}")
        return None

    def fetch_all(self, timeout: int = 10) -> Dict[str, Any]:
        """Fetch all registered sources.  Returns a dict keyed by URL."""
        results: Dict[str, Any] = {}
        for url in self.sources:
            data = self.fetch(url, timeout=timeout)
            if data is not None:
                results[url] = data
        return results

    def preprocess(self, data: Any) -> Any:
        """
        Minimal preprocessing: replace None values with 0 in dicts/lists.
        Extend this method with domain-specific logic as needed.
        """
        if isinstance(data, dict):
            return {k: (v if v is not None else 0) for k, v in data.items()}
        if isinstance(data, list):
            return [item if item is not None else 0 for item in data]
        return data

    def get_cached(self, url: str) -> Optional[Any]:
        """Return the last cached value for *url* without a new network call."""
        return self._cache.get(url)

    def clear_cache(self) -> None:
        self._cache.clear()

    def __repr__(self) -> str:
        return f"DataHandler(sources={self.sources})"
