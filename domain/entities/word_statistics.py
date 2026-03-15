from dataclasses import dataclass, field
from typing import Dict, List
from domain.value_objects.word import Word
from domain.value_objects.line_number import LineNumber


@dataclass
class WordStatistics:
    word: Word
    total_count: int = 0
    line_counts: Dict[int, int] = field(default_factory=dict)

    def add_occurrence(self, line_number: LineNumber) -> None:
        self.total_count += 1
        line_num = int(line_number)
        self.line_counts[line_num] = self.line_counts.get(line_num, 0) + 1

    def get_line_counts_list(self, total_lines: int) -> List[int]:
        return [self.line_counts.get(i, 0) for i in range(total_lines)]
