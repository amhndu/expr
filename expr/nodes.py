from abc import ABC, abstractmethod
from operator import add, sub, mul, truediv as div
from dataclasses import dataclass
from typing import Callable, ClassVar, Optional, Union, Any

Number = float


class Node(ABC):
    def __add__(self, node) -> 'Node':
        return BinaryOperation(operator=add, left=self, right=_node_or_constant(node))

    def __sub__(self, node) -> 'Node':
        return BinaryOperation(operator=sub, left=self, right=_node_or_constant(node))

    def __mul__(self, node) -> 'Node':
        return BinaryOperation(operator=mul, left=self, right=_node_or_constant(node))

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Number:
        raise NotImplementedError

    @abstractmethod
    def derivative(self, *args, **kwargs) -> Number:
        raise NotImplementedError


def _node_or_constant(val: Union[Node, Number]) -> Node:
    if isinstance(val, Node):
        return val
    return Constant(value=val)


@dataclass
class Constant(Node):
    value: Number

    def __call__(self, *args, **kwargs) -> Number:
        return self.value

    def derivative(self, *args, **kwargs) -> Number:
        return 0


@dataclass
class Variable(Node):
    name: Optional[str]
    index: Optional[int] = None

    def __post_init__(self):
        if self.name is None and self.index is None:
            raise ValueError("one of name or index must be set")

    def __call__(self, *args, **kwargs) -> Number:
        if self.name and self.name in kwargs:
            return kwargs[self.name]

        assert self.index is not None
        return args[self.index]

    def derivative(self, *args, **kwargs) -> Number:
        return 1


@dataclass
class BinaryOperation(Node):
    SUPPORTED_OPS: ClassVar = (add, sub, mul)

    operator: Callable[[Number, Number], Number]
    left: Node
    right: Node

    def __post_init__(self):
        if self.operator not in self.SUPPORTED_OPS:
            raise ValueError(f'unknown operator: {self.operator}, expecting one of {self.SUPPORTED_OPS}')

    def __call__(self, *args, **kwargs) -> Number:
        return self.operator(self.left(*args, **kwargs), self.right(*args, **kwargs))

    def derivative(self, *args, **kwargs) -> Number:
        if self.operator == add or self.operator == sub:
            return self.operator(self.left.derivative(*args, **kwargs), self.right.derivative(*args, **kwargs))
        elif self.operator == mul:
            left_val = self.left(*args, **kwargs)
            left_derivate = self.left.derivative(*args, **kwargs)
            right_val = self.right(*args, **kwargs)
            right_derivate = self.right.derivative(*args, **kwargs)
            return left_val * right_derivate + left_derivate * right_val

        raise Exception("unexpected operator")
