from abc import ABC, abstractmethod
from operator import add, sub, mul, truediv as div, pow
from dataclasses import dataclass
from typing import Callable, ClassVar, Optional, Union, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from expr.visitor import NodeVisitor, ResultT

Number = float

class Node(ABC):
    def __add__(self, node) -> 'Node':
        return BinaryOperation(operator=add, left=self, right=_node_or_constant(node))

    def __sub__(self, node) -> 'Node':
        return BinaryOperation(operator=sub, left=self, right=_node_or_constant(node))

    def __mul__(self, node) -> 'Node':
        return BinaryOperation(operator=mul, left=self, right=_node_or_constant(node))

    def __call__(self, *args, evaluator: 'Optional[NodeVisitor[ResultT]]'=None) -> 'ResultT':
        from expr.value import ValueVisitor
        if evaluator is None:
            evaluator = ValueVisitor()
        return self.calculate(*args, visitor=evaluator)

    @abstractmethod
    def calculate(self, *args, visitor: 'NodeVisitor[ResultT]') -> 'ResultT':
        raise NotImplementedError


def _node_or_constant(val: Node | Number) -> Node:
    if isinstance(val, Node):
        return val
    return Constant(constant=val)


@dataclass
class Constant(Node):
    constant: Number

    def calculate(self, *args, visitor: 'NodeVisitor[ResultT]') -> 'ResultT':
        return visitor.visit_constant(self, *args)




@dataclass
class Variable(Node):
    index: int

    def calculate(self, *args, visitor: 'NodeVisitor[ResultT]') -> 'ResultT':
        return visitor.visit_variable(self, *args)



@dataclass
class BinaryOperation(Node):
    SUPPORTED_OPS: ClassVar = (add, sub, mul, pow)

    operator: Callable[[Number, Number], Number]
    left: Node
    right: Node

    def __post_init__(self):
        if self.operator not in self.SUPPORTED_OPS:
            raise ValueError(f'unknown operator: {self.operator}, expecting one of {self.SUPPORTED_OPS}')

    def calculate(self, *args, visitor: 'NodeVisitor[ResultT]') -> 'ResultT':
        return visitor.visit_binary_operation(self, *args)

