from dataclasses import dataclass
import typing

from ...types import DotDict

@dataclass
class Task:
    name: str
    plugin: str|None
    args: DotDict[str, typing.Any]
    dep: list[str]
