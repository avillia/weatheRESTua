from fastapi import APIRouter

index = APIRouter()


@index.get("/", tags=["index", "main"])
def return_index():
    return {
        "status": "alive",
        "endpoints": ["/cities", "/mean", "/records", "/moving_mean"],
        "how_to_use": "Provide your arguments as query parameters!",
        "sample_request": "/records?start_dt=2021-12-17&end_dt=2021-12-18&city=Dnipro",
    }
