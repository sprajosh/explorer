from typing import List
import openai
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

class ChatProcessor:
    def __init__(self, api_key, file_path):
        openai.api_key = api_key
        self.file_path = file_path
        self.qa_chain = None

    def _load_data(self):
        if self.file_path.lower().endswith('.pdf'):
            return self._load_pdf()
        elif self.file_path.lower().endswith('.json'):
            return self._load_json()
        else:
            raise ValueError("Unsupported file type. Only PDF and JSON are supported.")

    def _load_pdf(self):
        pdf_loader = PyPDFLoader(self.file_path)
        pdf_data = pdf_loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        return text_splitter.split_documents(pdf_data)

    def _load_json(self):
        json_loader = JSONLoader(file_path=self.file_path, jq_schema='.[]', text_content=False)
        return json_loader.load()

    def _create_qa_chain(self, docs):
        embedding = OpenAIEmbeddings(openai_api_key=openai.api_key)
        vectorstore = Chroma.from_documents(documents=docs, embedding=embedding)
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=openai.api_key)

        messages = [
            SystemMessagePromptTemplate.from_template("Use the following context to answer the user's question. If you don't know the answer, just say that you don't know; don't try to make up an answer. {context} Begin! ---- Question: {question} Helpful Answer:"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)

        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": prompt}
        )

        return qa_chain

    def process_chat(self, questions: List[str]):
        if self.qa_chain is None:
            data = self._load_data()
            self.qa_chain = self._create_qa_chain(data)

        results = []
        for question in questions:
            result = self.qa_chain({"query": question})
            results.append(result)
        return results
