from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Word:
    value: str

    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Word must be a non-empty string")

    def is_valid(self) -> bool:
        return bool(re.match(r"^[а-яА-ЯёЁa-zA-Z]+$", self.value))

    def clean(self) -> str:
        return re.sub(r"[^\w]", "", self.value.lower())

    def __str__(self) -> str:
        return self.value
