from requests import status_codes

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Veriage - Age Verification</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #9f7aea 50%, #d6bcfa 100%);
            font-family: 'Quicksand', sans-serif;
            padding: 20px;
        }}

        .verification-container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(106, 13, 173, 0.3), 0 0 0 2px rgba(255, 255, 255, 0.1) inset;
            padding: 40px 50px;
            width: 100%;
            max-width: 450px;
            transition: transform 0.3s ease;
        }}

        .verification-container:hover {{
            transform: translateY(-5px);
        }}

        h1 {{
            font-family: 'Quicksand', sans-serif;
            font-size: 2.2rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #6b46c1 0%, #9f7aea 50%, #b794f4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        }}

        .subtitle {{
            text-align: center;
            color: #718096;
            margin-bottom: 30px;
            font-size: 0.95rem;
            font-weight: 400;
        }}

        form {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .input-group {{
            position: relative;
            width: 100%;
        }}

        .input-icon {{
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #9f7aea;
            font-size: 1.2rem;
        }}

        input[type='text'] {{
            width: 100%;
            padding: 16px 20px 16px 50px;
            border: 2px solid #e9d8fd;
            border-radius: 16px;
            font-size: 1rem;
            font-family: 'Quicksand', sans-serif;
            transition: all 0.3s ease;
            background: white;
            color: #2d3748;
            font-weight: 500;
        }}

        input[type='text']:focus {{
            outline: none;
            border-color: #9f7aea;
            box-shadow: 0 0 0 4px rgba(159, 122, 234, 0.2);
        }}

        input[type='text']::placeholder {{
            color: #cbd5e0;
            font-weight: 400;
        }}

        button {{
            background: linear-gradient(135deg, #805ad5 0%, #9f7aea 50%, #b794f4 100%);
            color: white;
            border: none;
            padding: 16px 30px;
            border-radius: 16px;
            font-size: 1.1rem;
            font-weight: 600;
            font-family: 'Quicksand', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(159, 122, 234, 0.4);
            letter-spacing: 0.5px;
            margin-top: 10px;
        }}

        button:hover {{
            background: linear-gradient(135deg, #6b46c1 0%, #805ad5 50%, #9f7aea 100%);
            box-shadow: 0 6px 20px rgba(106, 13, 173, 0.4);
            transform: scale(1.02);
        }}

        button:active {{
            transform: scale(0.98);
        }}

        .privacy-note {{
            text-align: center;
            margin-top: 20px;
            font-size: 0.85rem;
            color: #a0aec0;
        }}

        .privacy-note span {{
            color: #9f7aea;
            font-weight: 600;
        }}

        .decoration {{
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 20px;
        }}

        .dot {{
            width: 8px;
            height: 8px;
            background: #d6bcfa;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        .dot:nth-child(2) {{
            animation-delay: 0.3s;
            background: #9f7aea;
        }}

        .dot:nth-child(3) {{
            animation-delay: 0.6s;
            background: #805ad5;
        }}

        @keyframes pulse {{
            0%, 100% {{
                transform: scale(1);
                opacity: 0.5;
            }}
            50% {{
                transform: scale(1.5);
                opacity: 1;
            }}
        }}

        .hidden {{
            display: none;
        }}

        .result-message {{
            margin-top: 20px;
            padding: 12px;
            border-radius: 12px;
            font-size: 0.95rem;
            font-weight: 500;
            text-align: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .result-message.success {{
            background: #f0f4ff;
            color: #5a67d8;
            border-left: 4px solid #9f7aea;
            opacity: 1;
        }}

        .result-message.error {{
            background: #fff5f5;
            color: #c53030;
            border-left: 4px solid #fc8181;
            opacity: 1;
        }}
    </style>
</head>
<body>
    <div class="verification-container">
        <div class="decoration">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
        
        <h1>Veriage</h1>
        <div class="subtitle">Secure age verification</div>
        
        <form id='form'>
            <div class="input-group">
                <span class="input-icon">📱</span>
                <input 
                    type='text' 
                    name='number'
                    placeholder="Your phone number"
                    pattern="\+?[0-9]{10,15}"
                    title="Please enter a 15 digit number"
                    required
                >
            </div>
            <button type='button' id='submit'>Verify age</button>
        </form>
        
        <div id="result" class="result-message"></div>
    </div>

    <script>
        const button = document.getElementById('submit');
        const resultDiv = document.getElementById('result');

        button.addEventListener("click", async () => {{
            const form = document.getElementById('form');
            const formData = new FormData(form);
            const phoneNumber = formData.get('number');
            
            if (!phoneNumber || phoneNumber.length < 10) {{
                resultDiv.className = 'result-message error';
                resultDiv.textContent = 'Please enter a 15 characters valid number';
                return;
            }}
            
            const data = {{
                number: phoneNumber
            }};

            // Mostrar estado de carga
            button.textContent = 'Verifying...';
            button.disabled = true;
            
            try {{
                const response = await fetch('{HOST}/api/v1/validate', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify(data),
                }});
                
                const result = await response.json();
                console.log(result);

                if(!response.ok){{
                    resultDiv.className = 'result-message error';
                    resultDiv.textContent = '❌ An error has ocurred, try again.';
                }} else {{
                    resultDiv.className = 'result-message error';
                    resultDiv.classList.add('hidden');
                }}
                
                
            }} catch (error) {{
                console.error('Error:', error);
                resultDiv.className = 'result-message error';
                resultDiv.textContent = '❌ An error has ocurred, try again.';
            }} finally {{
                button.textContent = 'Verify age';
                button.disabled = false;
            }}
        }});

        document.getElementById('form').addEventListener('submit', (e) => {{
            e.preventDefault();
            button.click();
        }});
    </script>
</body>
</html>
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