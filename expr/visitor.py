from expr.nodes import Node, Number, Constant, Variable, BinaryOperation
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

ResultT = TypeVar('ResultT')

class NodeVisitor(ABC, Generic[ResultT]):
    """
        Visit a node tree and produce a value
    """

    @abstractmethod
    def visit_constant(self, node: Constant, *args) -> ResultT:
        raise NotImplementedError

    @abstractmethod
    def visit_variable(self, node: Variable, *args) -> ResultT:
        raise NotImplementedError

    @abstractmethod
    def visit_binary_operation(self, node: BinaryOperation, *args) -> ResultT:
        raise NotImplementedError
