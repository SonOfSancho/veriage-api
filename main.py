from fastapi import FastAPI, Path, Query
from fastapi.responses import Response, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

class TelNum(BaseModel):
    number: str

@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/widget", response_class=HTMLResponse)
async def get_auth_render():
    return """
        <form>
            <input type='tel'>
            <button type='button'></button>
        </form>

        <script>
            console.log("waos");
        </script>
    """

@app.post("api/v1/validate")
async def post_validation(number: TelNum):
    number_dict = number.model_dump()
    return number_dict.number