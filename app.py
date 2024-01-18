import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores.cassandra import Cassandra
from langchain_google_genai import ChatGoogleGenerativeAI
import cassio

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True,temperature=0.2)

prompt_template1="""
Elaborate Answer the question based only on given context:
Context: \n{context}\n
Question: \n{question}\n
Elaborate the answer giving all the information possible related to the question from the context in english, unless otherwise stated above.
Dont state about the context in the answer.
Answer:
"""
prompt1=PromptTemplate(template=prompt_template1,input_variables=["context","question"])

prompt_template2="""
Chat History: \n{chat_history}\n
{question}
"""
prompt2=PromptTemplate(template=prompt_template2,input_variables=["chat_history"])

def get_embeddings():
    return HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs={"device":"cpu"})

cassio.init(token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"), database_id=os.getenv("ASTRA_DB_ID"))
def get_vector_store():
    astra_vector_store=Cassandra(
        embedding=st.session_state.embeddings,
        table_name="qa_mini_demo",
        session=None,
        keyspace=None
    )
    return astra_vector_store

def get_conversation_chain():
    vectorstore=get_vector_store()
    memory = ConversationBufferWindowMemory(k=2, memory_key='chat_history', return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(llm=llm,
                                                  memory=memory,
                                                  verbose=True,
                                                  retriever=vectorstore.as_retriever(),
                                                  combine_docs_chain_kwargs={"prompt": prompt1},
                                                  chain_type="stuff",
                                                  )
    return chain

def handle_question(question,vectorstore):
    chain=st.session_state.chain
    res=chain({"question":question})
    st.session_state.chat_history=res["chat_history"]
    
    for i,msg in enumerate(st.session_state.chat_history):
        if i%2==0:
            st.chat_message("user",avatar='👨🏻‍💼').write(msg.content)
        else:
            st.chat_message("ai",avatar='🤖').write(msg.content)
    st.chat_message("user",avatar='👨🏻‍💼').write(question)
    st.chat_message("ai",avatar='🤖').write(res["answer"])


def main():
    st.set_page_config(page_title="MinBot", page_icon=":classical_building:")
    if "embeddings" not in st.session_state:
        st.session_state.embeddings=get_embeddings()
    if "chain" not in st.session_state:
        st.session_state.chain=get_conversation_chain()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[]
    vectorstore=get_vector_store()

    st.header(":male-construction-worker: :orange[Mine]B:blue[o]t.:green[:flag-in:]:", divider="grey")
    question=st.chat_input("🤖 Ask me anything about India's Mining Act rules and regulations.")
    if question:
        handle_question(question,vectorstore)
    
if __name__ == "__main__":
    main()