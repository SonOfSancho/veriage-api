from requests import status_codes

from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import Response, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from connection import swapverif, ageverif
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST")

app = FastAPI()

class TelNum(BaseModel):
    number: str

@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/widget", response_class=HTMLResponse)
async def get_auth_render():
    return f"""
<head>
</head>
<body>
    <form id='form'>
        <input type='tel' name='number'>
        <button type='button' id='submit'>Submit</button>
    </form>

    <script>
        const button = document.getElementById('submit');

        button.addEventListener("click", async () => {{
            const form = document.getElementById('form');
            const formData = new FormData(form);
            
            const data = {{
                number: formData.get('number')
            }};

            const response = await fetch('{HOST}/api/v1/validate', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify(data),
            }});
            
            const result = await response.json();
            console.log(result);
        }});
    </script>
</body>
    """

@app.post("/api/v1/validate")
async def post_validation(number: TelNum):
    phone = number.model_dump()["number"]

    simswap = swapverif(phone)
    
    if simswap == -1:
        raise HTTPException(status_code=404, detail="Phone not found")
    
    if simswap:
        raise HTTPException(status_code=406, detail="Phone doesn't meet the criteria")
    
    res = ageverif(phone)
    
    return res