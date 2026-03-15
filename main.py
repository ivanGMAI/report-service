from fastapi import FastAPI
from api.routers.report_router import router


app = FastAPI(
    title="Report Service",
    description="API for generating Excel reports from text files",
)
app.include_router(router)
