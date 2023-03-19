
from expr.visitor import NodeVisitor
from expr.nodes import Node, Number, BinaryOperation, Constant, Variable
from operator import add, sub, mul, truediv as div
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ValueVisitor(NodeVisitor):

    def visit_constant(self, node: Constant, *args) -> Number:
        return node.constant

    def visit_variable(self, node: Variable, *args) -> Number:
        return args[node.index]

    def visit_binary_operation(self, node: BinaryOperation, *args) -> Number:
        left_value = node.left.calculate(*args, visitor=self)
        right_value = node.right.calculate(*args, visitor=self)
        return node.operator(left_value, right_value)
