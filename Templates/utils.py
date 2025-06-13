"""
this code is about PDF reading and that too in a smaller chunks of text so models can only read and understand the text 
as much as the text fits in a context window 
"""

from langchain_community.document_loaders import PDFPlumberLoader
# extract text from page by page from pdf 
from langchain.text_splitter import RecursiveCharacterTextSplitter
# big text to smaller chunks 
# path of a PDF file I/p
def load_pdf_chunks(pdf_path):
    # load file
    loader = PDFPlumberLoader(pdf_path)
    # full text from each page and store in docs
    pages = loader.load()
    # splitter created to break chunks with their respective sizes
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # Returns the list of all text chunks. These can then be used for embedding, search, or question-answering
    return splitter.split_documents(pages)

