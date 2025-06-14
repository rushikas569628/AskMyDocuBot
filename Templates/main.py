from fastapi import FastAPI, File, UploadFile, Form
from Templates.agent import create_pdf_agent
import tempfile
from fastapi.responses import HTMLResponse

app = FastAPI()
@app.get("/")
def read_root():
    return {
        "message": "Welcome to AskMyDoc API!",
        "instructions": "Send a POST request to /ask/ with a PDF file and a question."
    }

@app.get("/form", response_class=HTMLResponse)
def form_page():
    return """
    <html>
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
