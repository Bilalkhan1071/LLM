# Import necessary libraries and modules
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader
from mangum import Mangum

# Initialize FastAPI
app = FastAPI()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Define OpenAI model for text embeddings
embed_model = "text-embedding-ada-002"

# Set Pinecone API key and environment
os.environ["PINECONE_API_KEY"] = "1f6a1881-f13f-4c62-a27a-5f202e3ea800"
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENV = "gcp-starter"

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len,
)

# Initialize Pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)

# Set Pinecone index name
index_name = 'pdftesterindex'

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Check if Pinecone index exists
if index_name not in pinecone.list_indexes():
    print(f'Index {index_name} does not exist')

# Initialize OpenAI language model
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

# PDF setup
loader = PyPDFLoader("/code/app/assets/ai_pdf_tester.pdf")
pdf_content = loader.load()
book_texts = text_splitter.split_documents(pdf_content)
book_docsearch = Pinecone.from_texts([t.page_content for t in book_texts], embeddings, index_name=index_name)

# PDF Query setup
chain = load_qa_chain(llm, chain_type="stuff")

# Define request model for queries
class QueryRequest(BaseModel):
    userprompt: str

# Define endpoint for running queries
@app.post("/query")
def run_query(query_request: QueryRequest):
    try:
        # Get user prompt from request
        userprompt = query_request.userprompt

        # Split PDF documents for search
        book_texts = text_splitter.split_documents(pdf_content)
        book_docsearch = Pinecone.from_texts([t.page_content for t in book_texts], embeddings, index_name=index_name)

        # Perform similarity search in Pinecone
        docs = book_docsearch.similarity_search(userprompt)

        # Run question answering chain
        output = chain.run(input_documents=docs, question=userprompt)
        return JSONResponse(content={"result": output})
    except Exception as e:
        # Handle exceptions and return error response
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Initialize Mangum for AWS Lambda deployment
handler = Mangum(app, lifespan="off")
