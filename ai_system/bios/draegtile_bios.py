"""
Draegtile BIOS
================
A pure-Python simulation of the Draegtile BIOS layer.

Responsibilities:
  - Power-On Self-Test (POST)
  - Hardware/environment discovery (CPU, OS, memory)
  - Security integrity check (hash of source files)
  - Module initialisation registry
  - Sensor simulation (temperature, frequency stubs)

Inspired by:
  - guides/Draegtile Bios.txt
  - guides/Draegtile overview.txt (boot sequence)
"""

import hashlib
import os
import platform
import time
from typing import Any, Dict, List, Optional


class DraegtileBIOS:
    """
    Simulated BIOS for the Draegtile AI system.

    Boot sequence:
      1. POST  – verify system health
      2. Memory / resource allocation
      3. I/O initialisation
      4. Security check
      5. Hand control to Draegtile OS layer (UnifiedSystem)
    """

    VERSION = "1.0.0-alpha"

    def __init__(self, watch_paths: Optional[List[str]] = None) -> None:
        self._watch_paths: List[str] = watch_paths or []
        self._baseline_hashes: Dict[str, str] = {}
        self._modules_registered: List[str] = []
        self._boot_log: List[str] = []

    # ------------------------------------------------------------------
    # Boot sequence
    # ------------------------------------------------------------------

    def boot(self) -> bool:
        """
        Run the full boot sequence.

        Returns
        -------
        bool
            True if all checks pass and the system is ready; False otherwise.
        """
        self._log(f"Draegtile BIOS v{self.VERSION} — starting boot sequence")
        ok = True
        ok = ok and self._post()
        ok = ok and self._init_memory()
        ok = ok and self._init_io()
        self._security_check()
        if ok:
            self._log("Boot complete. Transferring control to Draegtile OS.")
        else:
            self._log("Boot failed. System halted.")
        return ok

    # ------------------------------------------------------------------
    # POST
    # ------------------------------------------------------------------

    def _post(self) -> bool:
        self._log("[POST] Checking CPU ...")
        cpu = platform.processor() or "unknown"
        self._log(f"[POST]   CPU: {cpu}")

        self._log("[POST] Checking OS ...")
        os_name = f"{platform.system()} {platform.release()}"
        self._log(f"[POST]   OS: {os_name}")

        self._log("[POST] Checking Python runtime ...")
        import sys
        self._log(f"[POST]   Python: {sys.version.split()[0]}")

        self._log("[POST] POST complete — all checks passed.")
        return True

    # ------------------------------------------------------------------
    # Memory init
    # ------------------------------------------------------------------

    def _init_memory(self) -> bool:
        self._log("[MEM] Initialising memory allocation ...")
        # Record baseline hashes for watched source files
        for path in self._watch_paths:
            if os.path.isfile(path):
                self._baseline_hashes[path] = self._sha256(path)
        self._log(f"[MEM] {len(self._baseline_hashes)} source file(s) registered.")
        return True

    # ------------------------------------------------------------------
    # I/O init
    # ------------------------------------------------------------------

    def _init_io(self) -> bool:
        self._log("[I/O] Initialising standard I/O ...")
        self._log("[I/O] Sensor stubs ready (temperature, frequency).")
        return True

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------

    def _security_check(self) -> None:
        self._log("[SEC] Running integrity check ...")
        tampered = []
        for path, expected in self._baseline_hashes.items():
            current = self._sha256(path)
            if current != expected:
                tampered.append(path)
        if tampered:
            self._log(f"[SEC] WARNING — {len(tampered)} file(s) changed since baseline:")
            for t in tampered:
                self._log(f"[SEC]   {t}")
        else:
            self._log("[SEC] Integrity check passed.")

    # ------------------------------------------------------------------
    # Module registry
    # ------------------------------------------------------------------

    def register_module(self, name: str) -> None:
        """Register a Draegtile module as initialised."""
        self._modules_registered.append(name)
        self._log(f"[MODULE] Registered: {name}")

    def list_modules(self) -> List[str]:
        return list(self._modules_registered)

    # ------------------------------------------------------------------
    # Sensor stubs
    # ------------------------------------------------------------------

    @staticmethod
    def read_temperature() -> float:
        """Return a simulated temperature reading (°C)."""
        import random
        return round(20.0 + random.uniform(-2.0, 5.0), 2)

    @staticmethod
    def read_frequency() -> float:
        """Return a simulated frequency reading (Hz)."""
        import random
        return round(50.0 + random.uniform(-0.5, 0.5), 4)

    # ------------------------------------------------------------------
    # Hardware info
    # ------------------------------------------------------------------

    def get_hardware_status(self) -> Dict[str, Any]:
        return {
            "os": platform.system(),
            "os_version": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": platform.python_version(),
            "bios_version": self.VERSION,
        }

    # ------------------------------------------------------------------
    # Log helpers
    # ------------------------------------------------------------------

    def _log(self, message: str) -> None:
        ts = time.strftime("%H:%M:%S")
        entry = f"[{ts}] {message}"
        self._boot_log.append(entry)
        print(entry)

    def get_boot_log(self) -> List[str]:
        return list(self._boot_log)

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    @staticmethod
    def _sha256(path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def __repr__(self) -> str:
        return f"DraegtileBIOS(version={self.VERSION}, modules={self._modules_registered})"
