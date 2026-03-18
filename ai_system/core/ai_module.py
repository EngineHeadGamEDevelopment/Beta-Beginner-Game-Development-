"""
Draegtile AI Learning Module
==============================
A lightweight, self-learning AI module that does NOT depend on heavy
external ML frameworks so that the system runs without extra installs.

It uses a simple online-learning approach (incremental mean / linear
regression) to model patterns in incoming data and can:
  - Learn from new data samples
  - Predict the next value in a sequence
  - Detect anomalies (values far from the learned mean)
  - Self-repair by resetting learned weights when drift is too large
  - Optimise internal parameters over time

Inspired by:
  - guides/Python Detailer.txt (AI Learning Module)
  - guides/Draegtile overview.txt (AI.learn, AI.optimize, AI.self_repair)
  - guides/A unified project build.txt (AIModel class)
"""

import json
import math
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


class AILearningModule:
    """
    Lightweight, dependency-free self-learning AI module.

    The module tracks a running mean and variance for any named metric,
    performs simple linear-regression for trend prediction, detects
    anomalies and repairs itself when drift exceeds a threshold.
    """

    DRIFT_THRESHOLD = 3.0  # standard deviations before self-repair triggers

    def __init__(self, model_path: Optional[str] = None) -> None:
        self.model_path = model_path
        self._metrics: Dict[str, Dict[str, Any]] = {}
        self._log: List[Dict[str, Any]] = []
        if model_path and os.path.isfile(model_path):
            self._load(model_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def learn(self, label: str, value: float) -> None:
        """Update the model with a new labelled data point."""
        m = self._get_metric(label)
        m["count"] += 1
        n = m["count"]
        old_mean = m["mean"]
        m["mean"] += (value - old_mean) / n
        m["M2"] += (value - old_mean) * (value - m["mean"])
        m["samples"].append(value)
        if len(m["samples"]) > 100:
            m["samples"].pop(0)
        self._log_event("learn", {"label": label, "value": value})

    def predict(self, label: str) -> Optional[float]:
        """Predict the next value for a label using linear regression."""
        m = self._metrics.get(label)
        if m is None or m["count"] < 2:
            return None
        samples = m["samples"]
        n = len(samples)
        x_mean = (n - 1) / 2.0
        y_mean = sum(samples) / n
        numerator = sum((i - x_mean) * (s - y_mean) for i, s in enumerate(samples))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        if denominator == 0:
            return y_mean
        slope = numerator / denominator
        return y_mean + slope * (n - x_mean)

    def is_anomaly(self, label: str, value: float) -> bool:
        """Return True if *value* is anomalous (> DRIFT_THRESHOLD std-devs)."""
        m = self._metrics.get(label)
        if m is None or m["count"] < 2:
            return False
        std = self._std(m)
        if std == 0:
            return False
        z_score = abs(value - m["mean"]) / std
        return z_score > self.DRIFT_THRESHOLD

    def optimize(self) -> Dict[str, Any]:
        """
        Return a summary of learned metrics and flag any that have drifted.
        In a more advanced version this would adjust hyper-parameters.
        """
        summary = {}
        for label, m in self._metrics.items():
            summary[label] = {
                "count": m["count"],
                "mean": round(m["mean"], 4),
                "std": round(self._std(m), 4),
            }
        self._log_event("optimize", summary)
        return summary

    def self_repair(self, label: Optional[str] = None) -> None:
        """
        Reset learned state for *label* (or all labels if None) when drift
        is too large or data quality is poor.
        """
        targets = [label] if label else list(self._metrics.keys())
        for t in targets:
            if t in self._metrics:
                self._metrics[t] = self._blank_metric()
                self._log_event("self_repair", {"label": t})

    def save(self, path: Optional[str] = None) -> None:
        """Persist model state to a JSON file."""
        out = path or self.model_path
        if not out:
            raise ValueError("No model path specified.")
        with open(out, "w") as fh:
            json.dump({"metrics": self._metrics, "log": self._log[-50:]}, fh, indent=2)

    def get_log(self) -> List[Dict[str, Any]]:
        return list(self._log)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_metric(self, label: str) -> Dict[str, Any]:
        if label not in self._metrics:
            self._metrics[label] = self._blank_metric()
        return self._metrics[label]

    @staticmethod
    def _blank_metric() -> Dict[str, Any]:
        return {"count": 0, "mean": 0.0, "M2": 0.0, "samples": []}

    @staticmethod
    def _std(m: Dict[str, Any]) -> float:
        if m["count"] < 2:
            return 0.0
        variance = m["M2"] / (m["count"] - 1)
        return math.sqrt(max(variance, 0))

    def _log_event(self, event_type: str, details: Any) -> None:
        self._log.append(
            {
                "event": event_type,
                "details": details,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if len(self._log) > 500:
            self._log.pop(0)

    def _load(self, path: str) -> None:
        with open(path) as fh:
            state = json.load(fh)
        self._metrics = state.get("metrics", {})
        self._log = state.get("log", [])

    def __repr__(self) -> str:
        return f"AILearningModule(metrics={list(self._metrics.keys())})"
