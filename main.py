import os
import openai, langchain, pinecone
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader

app = FastAPI()

os.environ["OPENAI_API_KEY"] = "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"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

embed_model = "text-embedding-ada-002"

os.environ["PINECONE_API_KEY"] = "1f6a1881-f13f-4c62-a27a-5f202e3ea800"
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]   
PINECONE_ENV = "gcp-starter"



text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 0,
    length_function = len,
)

# # Pinecone setup


pinecone.init(
    api_key = PINECONE_API_KEY,
    environment = PINECONE_ENV
)

index_name = 'testsearchbook'

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
if index_name not in pinecone.list_indexes():
    print(f'Index {index_name} does not exist')


llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)


#PDF setup
loader = PyPDFLoader("assets/ai_pdf_tester.pdf")


pdf_content = loader.load()



book_texts = text_splitter.split_documents(pdf_content)
book_docsearch = Pinecone.from_texts([t.page_content for t in book_texts], embeddings, index_name = index_name)



#PDF Query setup

chain = load_qa_chain(llm, chain_type="stuff")

class QueryRequest(BaseModel):
    query: str



@app.post("/query")
async def run_query(query_request: QueryRequest):
    try:
        query = query_request.query
        docs = book_docsearch.similarity_search(query)
        output = chain.run(input_documents=docs, question=query)
        return JSONResponse(content={"result": output})
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

