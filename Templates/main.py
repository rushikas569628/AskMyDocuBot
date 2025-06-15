from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import tempfile
from Templates.agent import create_pdf_agent

import os

app = FastAPI()

# Serve static files like demo.mp4
app.mount("/static", StaticFiles(directory="Templates"), name="static")


@app.post("/ask/")
async def ask_question(file: UploadFile = File(...), question: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(await file.read())
        pdf_path = temp.name

    agent = create_pdf_agent(pdf_path)
    result = agent(question)

    answer = result['result']
    sources = [doc.page_content[:200] for doc in result['source_documents']]
    return {
        "answer": answer,
        "sources": sources
    }


@app.get("/form", response_class=HTMLResponse)
def form_page():
    return """
    <html>
        <head>
            <title>AskMyDoc - Form</title>
        </head>
        <body>
            <h2>AskMyDoc</h2>
            <form action="/ask/" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="application/pdf" required />
                <br/><br/>
                <textarea name="question" rows="4" cols="50" placeholder="Enter your question..." required></textarea>
                <br/><br/>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """


@app.get("/demo", response_class=HTMLResponse)
def demo_video():
    return """
    <html>
        <head>
            <title>AskMyDoc Demo</title>
        </head>
        <body style="font-family: Arial; text-align: center; padding: 40px;">
            <h2>🎥 AskMyDoc Video Demo</h2>
            <video width="720" height="480" controls>
                <source src="/static/demo.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <p style="margin-top: 20px; color: gray;">
                This is a self-hosted video demonstration of AskMyDoc.
            </p>
        </body>
    </html>
    """
