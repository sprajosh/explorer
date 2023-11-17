import openai

OPENAI_KEY = 'sk-'

openai.api_key = OPENAI_KEY


system_template = """Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}

Begin!
----------------
Question: {question}
Helpful Answer:"""

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]

prompt = ChatPromptTemplate.from_messages(messages)

# process pdf
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("sadhana paper.pdf")
data = loader.load()
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
docs = text_splitter.split_documents(data)

# process json
from langchain.document_loaders import JSONLoader
loader = JSONLoader(file_path='short.json', jq_schema='.[]', text_content=False)

# common retrival logic
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

embedding=OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
vectorstore = Chroma.from_documents(documents=docs,embedding=embedding)
from langchain.chat_models import ChatOpenAI

llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613",openai_api_key=OPENAI_KEY)
question = "What are the languages considered"
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), chain_type_kwargs = {"prompt": prompt})
result = qa_chain({"query": question})
