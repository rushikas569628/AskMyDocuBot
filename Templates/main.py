from fastapi import FastAPI, File, UploadFile, Form
from Templates.agent import create_pdf_agent
import tempfile

app = FastAPI()

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
