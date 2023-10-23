from dataclasses import dataclass
from typing import Callable

@dataclass
class MenuAction:
    name: str
    action: Callable
    args: list = None
    kwargs: dict = None

    def execute(self):
        if self.action is None:
            raise NotImplementedError("MenuAction.action == None ---> this action has not yet been implemented")

        if self.args is None:
            self.args = []
        if self.kwargs is None:
            self.kwargs = {}
        self.action(*self.args, **self.kwargs)
