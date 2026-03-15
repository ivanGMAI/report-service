import asyncio
import uuid
from datetime import datetime
from fastapi import UploadFile
from io import BytesIO
from domain.services.text_analyzer import TextAnalyzer
from infrastructure.file_readers.async_file_reader import AsyncFileReader
from infrastructure.repositories.excel_report_repository import ExcelReportRepository

analysis_semaphore = asyncio.Semaphore(2)


class GenerateReportUseCase:
    def __init__(
        self,
        analyzer: TextAnalyzer,
        file_reader: AsyncFileReader,
        repository: ExcelReportRepository,
    ):
        self.analyzer = analyzer
        self.file_reader = file_reader
        self.repository = repository

    def _generate_filename(self) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        short_uuid = uuid.uuid4().hex[:8]
        return f"report_{date_str}_{short_uuid}.xlsx"

    async def execute(self, file: UploadFile) -> tuple[BytesIO, str]:
        async with analysis_semaphore:
            lines = self.file_reader.read_lines(file)
            statistics = await self.analyzer.analyze(lines)
            total_lines = self.analyzer.get_total_lines()
            excel_file = self.repository.save(statistics, total_lines)
            filename = self._generate_filename()
            return excel_file, filename
