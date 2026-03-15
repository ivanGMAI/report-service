from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import StreamingResponse
from api.dependencies import get_generate_report_use_case, validate_txt_file
from application.use_cases.generate_report import GenerateReportUseCase

router = APIRouter(prefix="/public/report")


@router.post("/export")
async def export(
    file: UploadFile = Depends(validate_txt_file),
    use_case: GenerateReportUseCase = Depends(get_generate_report_use_case),
):
    excel_file, filename = await use_case.execute(file)

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
