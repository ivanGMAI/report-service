import uvicorn
from fastapi import FastAPI
from api.routers.report_router import router

app = FastAPI(
    title="Report Service",
    description="API for generating Excel reports from text files",
)
app.include_router(router)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
