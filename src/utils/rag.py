from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Load documents
path = os.environ.get('DOCS_PATH')
loader = DirectoryLoader(path, glob="**/*.md")
docs = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_splits = text_splitter.split_documents(docs)

# Initialize the embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Create vector store
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# Invoke the retriever

chat = ChatGoogleGenerativeAI(model="models/gemini-1.0-pro-latest", google_api_key=os.environ.get("GOOGLE_API_KEY"))

SYSTEM_TEMPLATE = """Answer the user's questions based on the below context.
 
If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know".
If the question is not clear, ask for clarification.
If the question is a general greeting, answer with a general greeting.
If the question is about code, answer with sample code.

Returns friendly and detailed answers with markdown format.

<context>
{context}
</context>
"""

question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "human",
            SYSTEM_TEMPLATE,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

document_chain = create_stuff_documents_chain(chat, question_answering_prompt)


def get_answer(question: str):
    """
    Get the answer to a question
    """
    context = retriever.invoke(question, top_k=4)
    print(len(context))
    print(context[0])

    answer = document_chain.invoke(
        {
            "context": context,
            "messages": [
                HumanMessage(content=question)
            ],
        }
    )
    return answer
