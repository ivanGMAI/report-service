from dataclasses import dataclass


@dataclass(frozen=True)
class LineNumber:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Line number cannot be negative")

    def __int__(self) -> int:
        return self.value
