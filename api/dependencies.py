from fastapi import UploadFile, HTTPException, File

from domain.services.lemmatizer import RussianLemmatizer
from domain.services.text_analyzer import TextAnalyzer
from infrastructure.file_readers.async_file_reader import AsyncFileReader
from infrastructure.repositories.excel_report_repository import ExcelReportRepository
from application.use_cases.generate_report import GenerateReportUseCase


def get_lemmatizer() -> RussianLemmatizer:
    return RussianLemmatizer()


def get_analyzer() -> TextAnalyzer:
    return TextAnalyzer(lemmatizer=get_lemmatizer())


def get_file_reader() -> AsyncFileReader:
    return AsyncFileReader()


def get_repository() -> ExcelReportRepository:
    return ExcelReportRepository()


def get_generate_report_use_case() -> GenerateReportUseCase:
    return GenerateReportUseCase(
        analyzer=get_analyzer(),
        file_reader=get_file_reader(),
        repository=get_repository(),
    )


def validate_txt_file(file: UploadFile = File(...)) -> UploadFile:
    if not file.filename or not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    return file
