from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.embeddings import CacheBackedEmbeddings
from langchain.memory import ChatMessageHistory
from langchain.storage import LocalFileStore
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

# Load documents
path = os.environ.get('DOCS_PATH')
print(path)
loader = DirectoryLoader(path, glob="**/*.md")
docs = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_splits = text_splitter.split_documents(docs)

# Initialize the embedding model
# embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
# embeddings = CohereEmbeddings(model="embed-english-light-v3.0")

underlying_embeddings = CohereEmbeddings(model="embed-english-light-v3.0")

store = LocalFileStore("./cache/")

embeddings = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)

# Create vector store
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# Invoke the retriever

# chat = ChatGoogleGenerativeAI(model="models/gemini-1.0-pro-latest", google_api_key=os.environ.get("GOOGLE_API_KEY"))
chat = ChatCohere(model="command")

SYSTEM_TEMPLATE = """
<context>
{context}
</context>
You are an experienced tutor for the Data Structures and Algorithms course.
Answer all questions to the best of your ability based on the above context.
If the question is not clear, ask for clarification.
If the context is not relevant, ignore it and answer the question as best as you can but inform the user that the context provided was not relevant to the question.

If the question is a general greeting, respond with a friendly greeting.

Provide friendly, informative answers using markdown format, ensuring clarity and engagement.
"""


question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_TEMPLATE,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = create_stuff_documents_chain(chat, question_answering_prompt)

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
)


def get_answer(question: str):
    """
    Get the answer to a question
    """
    global answer
    context = retriever.invoke(question, top_k=3)

    try:
        answer = (chain_with_message_history.invoke(
            {
                "context": context,
                "input": HumanMessage(question),
            },
            {"configurable": {"session_id": "unused"}}
        ))
    except Exception as e:
        print(e)
        answer = "You reached limit of the free version of the API. Please try again later."

    return answer
#
# questions = [
#     'my name is Vinh',
#     'what is my name',
#     'what did yoy say'
# ]
#
# for q in questions:
#     print(get_answer(q))
