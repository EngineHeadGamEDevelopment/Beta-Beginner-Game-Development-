"""
Draegtile Multi-Language Code Interpreter
==========================================
Executes scripts written in Python, JavaScript (Node.js), or C++
(via g++) in a safe subprocess.

Inspired by:
  - guides/Python Detailer.txt (CodeInterpreter class)
  - guides/A unified project build.txt (multi-language support)
"""

import os
import subprocess
import tempfile
from typing import Optional


SUPPORTED_LANGUAGES = {"python", "js", "cpp"}


class CodeInterpreter:
    """
    Run external scripts in Python, JavaScript, or C++.

    All executions are time-limited and their stdout/stderr are returned
    as strings so the caller can inspect or feed the output into the AI.
    """

    DEFAULT_TIMEOUT = 30  # seconds

    def run_file(
        self,
        language: str,
        script_path: str,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> dict:
        """
        Execute *script_path* using the interpreter for *language*.

        Returns
        -------
        dict with keys ``returncode``, ``stdout``, ``stderr``.
        """
        language = language.lower()
        if language not in SUPPORTED_LANGUAGES:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Unsupported language: {language}",
            }
        if not os.path.isfile(script_path):
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Script not found: {script_path}",
            }

        if language == "python":
            cmd = ["python", script_path]
        elif language == "js":
            cmd = ["node", script_path]
        elif language == "cpp":
            exe = script_path.replace(".cpp", "_out")
            compile_result = subprocess.run(
                ["g++", script_path, "-o", exe],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if compile_result.returncode != 0:
                return {
                    "returncode": compile_result.returncode,
                    "stdout": compile_result.stdout,
                    "stderr": compile_result.stderr,
                }
            cmd = [exe]

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def run_snippet(
        self,
        language: str,
        code: str,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> dict:
        """
        Execute an inline *code* snippet for the given *language*.
        Writes the snippet to a temporary file and delegates to ``run_file``.
        """
        language = language.lower()
        extensions = {"python": ".py", "js": ".js", "cpp": ".cpp"}
        ext = extensions.get(language, ".txt")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=ext, delete=False
        ) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            return self.run_file(language, tmp_path, timeout=timeout)
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    def __repr__(self) -> str:
        return f"CodeInterpreter(supported={sorted(SUPPORTED_LANGUAGES)})"
