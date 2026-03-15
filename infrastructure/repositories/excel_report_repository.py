from io import BytesIO
from openpyxl import Workbook
from typing import Dict
from domain.entities.word_statistics import WordStatistics


class ExcelReportRepository:

    def save(self, statistics: Dict[str, WordStatistics], total_lines: int) -> BytesIO:
        buffer = BytesIO()

        wb = Workbook(write_only=True)
        ws = wb.create_sheet()

        ws.append(["word", "total", "per_line"])

        for word, stats in sorted(statistics.items()):
            line_counts = stats.get_line_counts_list(total_lines)
            per_line = ",".join(map(str, line_counts))
            ws.append([word, stats.total_count, per_line])

        wb.save(buffer)

        buffer.seek(0)

        return buffer
