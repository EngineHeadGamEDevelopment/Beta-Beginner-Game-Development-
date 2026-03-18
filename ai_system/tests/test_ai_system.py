"""
Unit tests for the Draegtile AI System.

Run with:  python -m pytest ai_system/tests/ -v
"""

import sys
import os

# Ensure the repo root is on sys.path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import pytest
from ai_system.core.stack_machine import StackMachine, DimensionalStack
from ai_system.core.ai_module import AILearningModule
from ai_system.core.data_handler import DataHandler
from ai_system.core.user_interaction import UserInteraction
from ai_system.core.code_interpreter import CodeInterpreter
from ai_system.core.visualizer import Visualizer
from ai_system.game.rpg_game import RPGGame, Player


# ===========================================================================
# StackMachine
# ===========================================================================

class TestStackMachine:
    def test_push_pop(self):
        sm = StackMachine()
        sm.push(42)
        assert sm.pop() == 42

    def test_underflow(self):
        sm = StackMachine()
        with pytest.raises(IndexError):
            sm.pop()

    def test_add(self):
        sm = StackMachine()
        sm.push(10)
        sm.push(5)
        sm.add()
        assert sm.pop() == 15

    def test_sub(self):
        sm = StackMachine()
        sm.push(10)
        sm.push(3)
        sm.sub()
        assert sm.pop() == 7

    def test_mul(self):
        sm = StackMachine()
        sm.push(4)
        sm.push(5)
        sm.mul()
        assert sm.pop() == 20

    def test_div(self):
        sm = StackMachine()
        sm.push(10)
        sm.push(2)
        sm.div()
        assert sm.pop() == 5.0

    def test_div_by_zero(self):
        sm = StackMachine()
        sm.push(10)
        sm.push(0)
        with pytest.raises(ZeroDivisionError):
            sm.div()

    def test_duplicate(self):
        sm = StackMachine()
        sm.push(7)
        sm.duplicate()
        assert sm.pop() == 7
        assert sm.pop() == 7

    def test_swap(self):
        sm = StackMachine()
        sm.push(1)
        sm.push(2)
        sm.swap()
        assert sm.pop() == 1
        assert sm.pop() == 2

    def test_clear(self):
        sm = StackMachine()
        sm.push(1)
        sm.push(2)
        sm.clear()
        with pytest.raises(IndexError):
            sm.pop()

    def test_execute_instructions(self):
        sm = StackMachine()
        sm.execute(["PUSH", "10", "PUSH", "20", "ADD"])
        assert sm.peek() == 30

    def test_execute_unknown_instruction(self, capsys):
        sm = StackMachine()
        sm.execute(["UNKNOWN"])
        out = capsys.readouterr().out
        assert "Unknown instruction" in out


# ===========================================================================
# DimensionalStack
# ===========================================================================

class TestDimensionalStack:
    def test_1d(self):
        ds = DimensionalStack((5,))
        ds.set_value(2, value=99)
        assert ds.get_value(2) == 99

    def test_2d(self):
        ds = DimensionalStack((3, 3))
        ds.set_value(1, 2, value=42)
        assert ds.get_value(1, 2) == 42

    def test_3d(self):
        ds = DimensionalStack((3, 3, 3))
        ds.set_value(2, 2, 2, value=7)
        assert ds.get_value(2, 2, 2) == 7

    def test_invalid_dims(self):
        with pytest.raises(ValueError):
            DimensionalStack((2, 2, 2, 2))

    def test_index_mismatch(self):
        ds = DimensionalStack((3, 3))
        with pytest.raises(IndexError):
            ds.get_value(0)


# ===========================================================================
# AILearningModule
# ===========================================================================

class TestAILearningModule:
    def test_learn_and_predict(self):
        ai = AILearningModule()
        for v in [1, 3, 5, 7, 9]:
            ai.learn("seq", float(v))
        pred = ai.predict("seq")
        # Trend is +2 per step, so next should be ~ 11
        assert pred is not None
        assert 9 < pred < 15

    def test_no_prediction_without_data(self):
        ai = AILearningModule()
        assert ai.predict("unknown") is None

    def test_anomaly_detection(self):
        ai = AILearningModule()
        for v in range(10):
            ai.learn("m", float(v))
        assert ai.is_anomaly("m", 10000.0) is True
        assert ai.is_anomaly("m", 5.0) is False

    def test_self_repair(self):
        ai = AILearningModule()
        for v in range(5):
            ai.learn("x", float(v))
        ai.self_repair("x")
        assert ai.predict("x") is None

    def test_optimize_returns_dict(self):
        ai = AILearningModule()
        ai.learn("a", 1.0)
        ai.learn("a", 2.0)
        summary = ai.optimize()
        assert "a" in summary
        assert "mean" in summary["a"]

    def test_save_load(self, tmp_path):
        ai = AILearningModule()
        ai.learn("t", 1.0)
        ai.learn("t", 2.0)
        path = str(tmp_path / "model.json")
        ai.save(path)
        ai2 = AILearningModule(model_path=path)
        assert "t" in ai2._metrics


# ===========================================================================
# DataHandler
# ===========================================================================

class TestDataHandler:
    def test_add_source(self):
        dh = DataHandler()
        dh.add_source("http://example.com/a")
        assert "http://example.com/a" in dh.sources

    def test_no_duplicate_source(self):
        dh = DataHandler(["http://x.com"])
        dh.add_source("http://x.com")
        assert dh.sources.count("http://x.com") == 1

    def test_preprocess_dict(self):
        dh = DataHandler()
        out = dh.preprocess({"a": 1, "b": None, "c": 3})
        assert out["b"] == 0
        assert out["a"] == 1

    def test_preprocess_list(self):
        dh = DataHandler()
        out = dh.preprocess([1, None, 3])
        assert out == [1, 0, 3]

    def test_cache_miss(self):
        dh = DataHandler()
        assert dh.get_cached("http://not-fetched.com") is None


# ===========================================================================
# UserInteraction
# ===========================================================================

class TestUserInteraction:
    def test_log_and_history(self):
        ui = UserInteraction()
        ui.log("command", {"text": "go north"})
        history = ui.get_history()
        assert len(history) == 1
        assert history[0]["event"] == "command"

    def test_recent(self):
        ui = UserInteraction()
        for i in range(20):
            ui.log("e", i)
        recent = ui.get_recent(5)
        assert len(recent) == 5
        assert recent[-1]["details"] == 19

    def test_hook_fires(self):
        ui = UserInteraction()
        received = []
        ui.on("click", lambda e: received.append(e))
        ui.log("click", "button_a")
        assert len(received) == 1

    def test_clear_history(self):
        ui = UserInteraction()
        ui.log("e", 1)
        ui.clear_history()
        assert ui.get_history() == []


# ===========================================================================
# CodeInterpreter
# ===========================================================================

class TestCodeInterpreter:
    def test_run_python_snippet(self):
        ci = CodeInterpreter()
        result = ci.run_snippet("python", 'print("hello")')
        assert result["returncode"] == 0
        assert "hello" in result["stdout"]

    def test_unsupported_language(self):
        ci = CodeInterpreter()
        result = ci.run_snippet("ruby", "puts 'hi'")
        assert result["returncode"] == -1
        assert "Unsupported" in result["stderr"]

    def test_missing_file(self):
        ci = CodeInterpreter()
        result = ci.run_file("python", "/nonexistent/path.py")
        assert result["returncode"] == -1

    def test_python_error_captured(self):
        ci = CodeInterpreter()
        result = ci.run_snippet("python", "raise ValueError('oops')")
        assert result["returncode"] != 0
        assert "oops" in result["stderr"]


# ===========================================================================
# Visualizer
# ===========================================================================

class TestVisualizer:
    def test_ascii_render_does_not_raise(self, capsys):
        vis = Visualizer()
        ds = DimensionalStack((2, 2))
        ds.set_value(0, 0, value=1)
        vis.visualize_stack(ds, title="Test")
        captured = capsys.readouterr()
        assert "Test" in captured.out

    def test_graph_plot_ascii(self, capsys):
        vis = Visualizer()
        # Force ASCII by temporarily hiding matplotlib
        vis._plt = None
        vis.graph_plot([1.0, 2.0, 3.0], title="Line")
        captured = capsys.readouterr()
        assert "Line" in captured.out


# ===========================================================================
# RPGGame
# ===========================================================================

class TestRPGGame:
    def setup_method(self):
        self.game = RPGGame()
        self.game.new_game("Tester", "Warrior")

    def test_new_game_sets_player(self):
        assert self.game.player is not None
        assert self.game.player.name == "Tester"

    def test_look_command(self):
        out = self.game.command("look")
        assert "village" in out.lower() or "exits" in out.lower()

    def test_move_valid(self):
        out = self.game.command("go north")
        assert "forest" in out.lower() or "north" in out.lower()

    def test_move_invalid(self):
        out = self.game.command("go west")
        assert "can't" in out.lower()

    def test_status_command(self):
        out = self.game.command("status")
        assert "Tester" in out

    def test_help_command(self):
        out = self.game.command("help")
        assert "look" in out

    def test_inventory_empty(self):
        out = self.game.command("inventory")
        assert "empty" in out.lower()

    def test_pick_nonexistent_item(self):
        out = self.game.command("pick dragon_egg")
        assert "no" in out.lower() or "there is" in out.lower()

    def test_unknown_command(self):
        out = self.game.command("dance")
        assert "unknown" in out.lower()

    def test_player_gain_xp_level_up(self):
        p = Player("Hero")
        msg = p.gain_xp(1000)
        assert "LEVEL UP" in msg
        assert p.level > 1

    def test_player_use_healing_potion(self):
        p = Player("Hero")
        p.hp = 50
        p.inventory.append("healing_potion")
        msg = p.use_item("healing_potion")
        assert "recovered" in msg
        assert p.hp > 50

    def test_player_use_nonexistent_item(self):
        p = Player("Hero")
        msg = p.use_item("magic_wand")
        assert "don't have" in msg
