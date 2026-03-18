"""
Draegtile Stack-Based Virtual Machine
======================================
Implements the core stack machine described in the Draegtile guides.
Supports 1-D through 3-D dimensional stacks and a basic instruction set.

Inspired by:
  - guides/Draegtile overview.txt (stack commands, dimensional data)
  - guides/Draegtile programming language and commands with a basic bios structure.txt
"""

from typing import Any, List, Optional


class DimensionalStack:
    """A multi-dimensional data stack (1D, 2D, or 3D)."""

    def __init__(self, dimensions: tuple):
        if len(dimensions) == 1:
            self.data: Any = [0] * dimensions[0]
        elif len(dimensions) == 2:
            self.data = [[0] * dimensions[1] for _ in range(dimensions[0])]
        elif len(dimensions) == 3:
            self.data = [
                [[0] * dimensions[2] for _ in range(dimensions[1])]
                for _ in range(dimensions[0])
            ]
        else:
            raise ValueError("Only 1D, 2D, and 3D stacks are supported.")
        self.dimensions = dimensions

    def set_value(self, *indices, value: Any) -> None:
        """Set a value at the given indices."""
        if len(indices) != len(self.dimensions):
            raise IndexError("Index count must match the number of dimensions.")
        if len(indices) == 1:
            self.data[indices[0]] = value
        elif len(indices) == 2:
            self.data[indices[0]][indices[1]] = value
        elif len(indices) == 3:
            self.data[indices[0]][indices[1]][indices[2]] = value

    def get_value(self, *indices) -> Any:
        """Get a value at the given indices."""
        if len(indices) != len(self.dimensions):
            raise IndexError("Index count must match the number of dimensions.")
        if len(indices) == 1:
            return self.data[indices[0]]
        elif len(indices) == 2:
            return self.data[indices[0]][indices[1]]
        elif len(indices) == 3:
            return self.data[indices[0]][indices[1]][indices[2]]

    def __repr__(self) -> str:
        return f"DimensionalStack(dimensions={self.dimensions}, data={self.data})"


class StackMachine:
    """
    A simple stack-based virtual machine that executes Draegtile instructions.

    Supported instructions:
      PUSH <value>   – push a value onto the stack
      POP            – pop and print the top value
      DUPLICATE      – duplicate the top value
      SWAP           – swap the top two values
      ADD            – pop two values, push their sum
      SUB            – pop two values, push their difference
      MUL            – pop two values, push their product
      DIV            – pop two values, push their quotient
      PRINT          – print the top value without popping
      CLEAR          – clear the stack
    """

    def __init__(self) -> None:
        self._stack: List[Any] = []

    # ------------------------------------------------------------------
    # Low-level stack operations
    # ------------------------------------------------------------------

    def push(self, value: Any) -> None:
        self._stack.append(value)

    def pop(self) -> Any:
        if not self._stack:
            raise IndexError("Stack underflow: nothing to pop.")
        return self._stack.pop()

    def peek(self) -> Any:
        if not self._stack:
            raise IndexError("Stack is empty.")
        return self._stack[-1]

    def duplicate(self) -> None:
        self.push(self.peek())

    def swap(self) -> None:
        if len(self._stack) < 2:
            raise IndexError("Not enough values on the stack to swap.")
        self._stack[-1], self._stack[-2] = self._stack[-2], self._stack[-1]

    def clear(self) -> None:
        self._stack.clear()

    # ------------------------------------------------------------------
    # Arithmetic
    # ------------------------------------------------------------------

    def add(self) -> None:
        b, a = self.pop(), self.pop()
        self.push(a + b)

    def sub(self) -> None:
        b, a = self.pop(), self.pop()
        self.push(a - b)

    def mul(self) -> None:
        b, a = self.pop(), self.pop()
        self.push(a * b)

    def div(self) -> None:
        b, a = self.pop(), self.pop()
        if b == 0:
            raise ZeroDivisionError("Division by zero in stack machine.")
        self.push(a / b)

    # ------------------------------------------------------------------
    # Instruction execution
    # ------------------------------------------------------------------

    def execute(self, instructions: List[str]) -> None:
        """Execute a list of string instructions."""
        idx = 0
        while idx < len(instructions):
            token = instructions[idx].upper()
            if token == "PUSH":
                idx += 1
                self.push(self._parse_value(instructions[idx]))
            elif token == "POP":
                print(f"[POP] {self.pop()}")
            elif token == "DUPLICATE":
                self.duplicate()
            elif token == "SWAP":
                self.swap()
            elif token == "ADD":
                self.add()
            elif token == "SUB":
                self.sub()
            elif token == "MUL":
                self.mul()
            elif token == "DIV":
                self.div()
            elif token == "PRINT":
                print(f"[STACK TOP] {self.peek()}")
            elif token == "CLEAR":
                self.clear()
            else:
                print(f"[WARNING] Unknown instruction: {token}")
            idx += 1

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_value(raw: str) -> Any:
        """Try to convert a string to int/float, otherwise keep as string."""
        try:
            return int(raw)
        except ValueError:
            pass
        try:
            return float(raw)
        except ValueError:
            pass
        return raw

    def __repr__(self) -> str:
        return f"StackMachine(stack={self._stack})"
