import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores.cassandra import Cassandra
import cassio

path=os.path.join(os.curdir,"ChatbotDataset/")
docs=os.listdir(path)

def get_text_chunks(docs):
    text=""
    for doc in docs:
        pdf=PdfReader(os.path.join(path,doc))
        for page in pdf.pages:
            text+=page.extract_text()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks=text_splitter.split_text(text)
    return chunks

chunks=get_text_chunks(docs)

instruct_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs={"device":"cpu"})

load_dotenv()
cassio.init(token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"), database_id=os.getenv("ASTRA_DB_ID"))

astra_vector_store=Cassandra(
    embedding=instruct_embeddings,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None
)

astra_vector_store.add_texts(chunks)
