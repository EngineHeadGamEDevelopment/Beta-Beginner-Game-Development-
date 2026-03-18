"""
Draegtile AI System — Unified Entry Point
==========================================
Ties together all core modules:
  - DraegtileBIOS  (boot / hardware)
  - StackMachine / DimensionalStack
  - AILearningModule
  - DataHandler
  - UserInteraction
  - CodeInterpreter
  - Visualizer
  - RPGGame

Run directly for an interactive demo:

    python main.py

Inspired by:
  - guides/Python Detailer.txt (UnifiedSystem)
  - guides/A unified project build.txt
"""

import os
import sys
from typing import Optional

# Ensure the package root is on the path when running directly
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from ai_system.bios.draegtile_bios import DraegtileBIOS
from ai_system.core.ai_module import AILearningModule
from ai_system.core.code_interpreter import CodeInterpreter
from ai_system.core.data_handler import DataHandler
from ai_system.core.stack_machine import DimensionalStack, StackMachine
from ai_system.core.user_interaction import UserInteraction
from ai_system.core.visualizer import Visualizer
from ai_system.game.rpg_game import RPGGame


class DraegtileSystem:
    """
    The unified Draegtile AI system.

    Initialise and boot the BIOS, then expose all sub-systems through a
    single interface.
    """

    def __init__(self, model_path: Optional[str] = None) -> None:
        # Collect source files for integrity tracking
        source_files = [
            os.path.join(_HERE, "core", "ai_module.py"),
            os.path.join(_HERE, "core", "stack_machine.py"),
            os.path.join(_HERE, "core", "data_handler.py"),
            os.path.join(_HERE, "core", "user_interaction.py"),
            os.path.join(_HERE, "core", "code_interpreter.py"),
            os.path.join(_HERE, "core", "visualizer.py"),
            os.path.join(_HERE, "game", "rpg_game.py"),
            os.path.join(_HERE, "bios", "draegtile_bios.py"),
        ]

        self.bios = DraegtileBIOS(watch_paths=source_files)
        self.ai = AILearningModule(model_path=model_path)
        self.data = DataHandler()
        self.stack_machine = StackMachine()
        self.user = UserInteraction()
        self.interpreter = CodeInterpreter()
        self.visualizer = Visualizer()
        self.game = RPGGame()

    # ------------------------------------------------------------------
    # Boot
    # ------------------------------------------------------------------

    def boot(self) -> bool:
        """Run BIOS boot sequence and register all modules."""
        ok = self.bios.boot()
        if ok:
            for name in [
                "AILearningModule",
                "DataHandler",
                "StackMachine",
                "UserInteraction",
                "CodeInterpreter",
                "Visualizer",
                "RPGGame",
            ]:
                self.bios.register_module(name)
        return ok

    # ------------------------------------------------------------------
    # Quick-access helpers
    # ------------------------------------------------------------------

    def run_stack_demo(self) -> None:
        """Demonstrate the stack machine with a sample instruction sequence."""
        print("\n--- Stack Machine Demo ---")
        instructions = [
            "PUSH", "10",
            "PUSH", "20",
            "ADD",
            "PRINT",
            "PUSH", "3",
            "MUL",
            "PRINT",
        ]
        self.stack_machine.execute(instructions)

    def run_ai_demo(self) -> None:
        """Feed some sample data into the AI module and show predictions."""
        print("\n--- AI Learning Demo ---")
        samples = [1, 3, 5, 7, 9, 11, 13]
        for v in samples:
            self.ai.learn("sequence", float(v))
        prediction = self.ai.predict("sequence")
        print(f"  Learned from: {samples}")
        print(f"  Predicted next value: {prediction}")
        anomaly = self.ai.is_anomaly("sequence", 1000.0)
        print(f"  Is 1000 an anomaly? {anomaly}")
        summary = self.ai.optimize()
        print(f"  Optimisation summary: {summary}")

    def run_3d_stack_demo(self) -> None:
        """Create a 3-D stack, fill it with data and visualise it."""
        print("\n--- 3-D Dimensional Stack Demo ---")
        cube = DimensionalStack((3, 3, 3))
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    cube.set_value(x, y, z, value=(x + 1) * (y + 1) * (z + 1))
        self.ai.learn("cube_value", float(cube.get_value(1, 1, 1)))
        self.visualizer.visualize_stack(cube, title="3-D Cube Stack")

    def start_rpg(self) -> None:
        """Start the interactive RPG game."""
        self.game.start()

    # ------------------------------------------------------------------
    # Interactive menu
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Interactive top-level menu."""
        if not self.boot():
            print("System failed to boot. Exiting.")
            return

        menu = (
            "\n========================================\n"
            "  Draegtile AI System — Main Menu\n"
            "========================================\n"
            "  1. Run Stack Machine Demo\n"
            "  2. Run AI Learning Demo\n"
            "  3. Run 3-D Dimensional Stack Demo\n"
            "  4. Play RPG Game\n"
            "  5. Show Hardware Status\n"
            "  6. Exit\n"
        )

        while True:
            print(menu)
            try:
                choice = input("Select an option: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye.")
                break

            if choice == "1":
                self.run_stack_demo()
            elif choice == "2":
                self.run_ai_demo()
            elif choice == "3":
                self.run_3d_stack_demo()
            elif choice == "4":
                self.start_rpg()
            elif choice == "5":
                status = self.bios.get_hardware_status()
                for k, v in status.items():
                    print(f"  {k}: {v}")
            elif choice == "6":
                print("Shutting down Draegtile AI System. Goodbye.")
                break
            else:
                print("  Invalid option. Please choose 1-6.")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    system = DraegtileSystem()
    system.run()
