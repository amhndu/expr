from expr.visitor import NodeVisitor
from expr.value import ValueVisitor
from expr.nodes import Node, Number, BinaryOperation
from operator import add, sub, mul, truediv as div, pow
from typing import Dict, List, ClassVar
from dataclasses import dataclass

@dataclass
class Differentiator(NodeVisitor):
    value_visitor: ClassVar[NodeVisitor] = ValueVisitor()

    def visit_constant(self, node, *args) -> Number:
        return 0

    def visit_variable(self, node, *args) -> Number:
        return 1

    def visit_binary_operation(self, node: BinaryOperation, *args) -> Number:
        if node.operator == add or node.operator == sub:
            left_value = node.left.calculate(*args, visitor=self)
            right_value = node.right.calculate(*args, visitor=self)
            return node.operator(left_value, right_value)

        elif node.operator == mul:
            left_value = node.left.calculate(*args, visitor=self.value_visitor)
            left_derivate = node.left.calculate(*args, visitor=self)
            right_value = node.right.calculate(*args, visitor=self.value_visitor)
            right_derivate = node.right.calculate(*args, visitor=self)
            return left_value * right_derivate + left_derivate * right_value

        raise Exception("unexpected operator")
