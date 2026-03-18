"""
Draegtile User Interaction Module
====================================
Tracks and logs user interactions, feeding them back to the AI for
continuous learning and adaptation.

Inspired by:
  - guides/Python Detailer.txt (UserInteraction class)
  - guides/Draegtile user.txt
"""

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


class UserInteraction:
    """
    Records user events (commands, inputs, choices) with timestamps and
    makes the history available for AI learning.
    """

    def __init__(self) -> None:
        self._history: List[Dict[str, Any]] = []
        self._hooks: Dict[str, List[Callable]] = {}

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def log(self, event_type: str, details: Any = None) -> None:
        """
        Record an interaction event.

        Parameters
        ----------
        event_type : str
            A short label for the event (e.g. ``"command"``, ``"choice"``).
        details : any
            Arbitrary data associated with the event.
        """
        entry: Dict[str, Any] = {
            "event": event_type,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        }
        self._history.append(entry)
        self._fire_hooks(event_type, entry)

    # ------------------------------------------------------------------
    # History access
    # ------------------------------------------------------------------

    def get_history(self) -> List[Dict[str, Any]]:
        """Return a copy of the full interaction history."""
        return list(self._history)

    def get_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        """Return the *n* most recent events."""
        return list(self._history[-n:])

    def clear_history(self) -> None:
        self._history.clear()

    # ------------------------------------------------------------------
    # Hooks (event callbacks)
    # ------------------------------------------------------------------

    def on(self, event_type: str, callback: Callable) -> None:
        """Register *callback* to be called whenever *event_type* is logged."""
        self._hooks.setdefault(event_type, []).append(callback)

    def _fire_hooks(self, event_type: str, entry: Dict[str, Any]) -> None:
        for cb in self._hooks.get(event_type, []):
            try:
                cb(entry)
            except Exception as exc:
                print(f"[UserInteraction] Hook error for '{event_type}': {exc}")

    # ------------------------------------------------------------------
    # Simple input helper
    # ------------------------------------------------------------------

    def prompt(self, message: str, event_type: str = "input") -> str:
        """
        Display *message* to the user, record the response and return it.
        """
        response = input(message)
        self.log(event_type, {"prompt": message, "response": response})
        return response

    def __repr__(self) -> str:
        return f"UserInteraction(events_logged={len(self._history)})"
