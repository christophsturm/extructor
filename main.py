import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, HttpUrl
import extruct
import requests
app = FastAPI()


# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/extract")
async def extract_microformats(url: HttpUrl):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(str(url))
        html_content = response.text

        data = extruct.extract(html_content, base_url=str(url),
                               syntaxes=['microdata', 'json-ld', 'opengraph', 'microformat'])

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)