"""
Draegtile 3-D Visualiser (text fallback)
==========================================
Provides a lightweight ASCII/text-based visualisation of DimensionalStack
data so the system works without any graphical dependencies.

If PyVista or Matplotlib is available it will use them; otherwise it
gracefully falls back to an ASCII representation.

Inspired by:
  - guides/Python Detailer.txt (Visualizer3D class)
  - guides/Draegtile overview.txt (visualize_stack, render_3D, graph_plot)
"""

from typing import Any, List, Optional


def _try_import_pyvista():
    try:
        import pyvista as pv  # type: ignore
        return pv
    except ImportError:
        return None


def _try_import_matplotlib():
    try:
        import matplotlib.pyplot as plt  # type: ignore
        return plt
    except ImportError:
        return None


class Visualizer:
    """
    Visualise stack data.

    - If PyVista is installed a 3-D mesh window is shown.
    - If Matplotlib is installed a 2-D or 3-D plot is shown.
    - Otherwise data is printed as an ASCII table.
    """

    def __init__(self) -> None:
        self._pv = _try_import_pyvista()
        self._plt = _try_import_matplotlib()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def visualize_stack(self, stack: Any, title: str = "Stack Data") -> None:
        """Display the contents of *stack* using the best available method."""
        if hasattr(stack, "data"):
            data = stack.data
        else:
            data = stack

        dims = self._detect_dims(data)
        if dims == 3 and self._pv is not None:
            self._render_3d_pyvista(data, title)
        elif self._plt is not None:
            self._render_matplotlib(data, dims, title)
        else:
            self._render_ascii(data, title)

    def render_3d(self, stack: Any, title: str = "3-D Render") -> None:
        """Alias for 3-D focused rendering."""
        self.visualize_stack(stack, title=title)

    def graph_plot(self, values: List[float], title: str = "Plot") -> None:
        """Plot a 1-D list of values."""
        if self._plt is not None:
            plt = self._plt
            plt.figure()
            plt.plot(values, marker="o")
            plt.title(title)
            plt.xlabel("Index")
            plt.ylabel("Value")
            plt.tight_layout()
            plt.show()
        else:
            print(f"\n{title}")
            for i, v in enumerate(values):
                bar = "#" * int(abs(v))
                print(f"  [{i:3d}] {bar} {v}")

    # ------------------------------------------------------------------
    # Rendering backends
    # ------------------------------------------------------------------

    def _render_3d_pyvista(self, data: Any, title: str) -> None:
        pv = self._pv
        import numpy as np  # type: ignore
        try:
            pts = np.array(
                [
                    [x, y, data[x][y][0]]
                    for x in range(len(data))
                    for y in range(len(data[0]))
                ],
                dtype=float,
            )
            mesh = pv.PolyData(pts)
            plotter = pv.Plotter(title=title)
            plotter.add_mesh(mesh, point_size=8, render_points_as_spheres=True)
            plotter.show()
        except Exception as exc:
            print(f"[Visualizer] PyVista render failed: {exc}")
            self._render_ascii(data, title)

    def _render_matplotlib(self, data: Any, dims: int, title: str) -> None:
        plt = self._plt
        try:
            if dims == 1:
                plt.figure()
                plt.plot(data, marker="o")
                plt.title(title)
                plt.show()
            elif dims == 2:
                plt.figure()
                plt.imshow(data, aspect="auto")
                plt.colorbar()
                plt.title(title)
                plt.show()
            else:
                self._render_ascii(data, title)
        except Exception as exc:
            print(f"[Visualizer] Matplotlib render failed: {exc}")
            self._render_ascii(data, title)

    @staticmethod
    def _render_ascii(data: Any, title: str) -> None:
        print(f"\n{'='*40}")
        print(f"  {title}")
        print(f"{'='*40}")
        if isinstance(data, list):
            for row in data:
                print(f"  {row}")
        else:
            print(f"  {data}")
        print(f"{'='*40}\n")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_dims(data: Any) -> int:
        if not isinstance(data, list):
            return 0
        if not isinstance(data[0], list):
            return 1
        if not isinstance(data[0][0], list):
            return 2
        return 3

    def __repr__(self) -> str:
        backends = []
        if self._pv:
            backends.append("pyvista")
        if self._plt:
            backends.append("matplotlib")
        if not backends:
            backends.append("ascii")
        return f"Visualizer(backends={backends})"
