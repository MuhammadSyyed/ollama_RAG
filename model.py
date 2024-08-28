import chromadb
import logging
import sys

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    Settings, VectorStoreIndex, SimpleDirectoryReader, PromptTemplate)
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


global query_engine
query_engine = None


def init_llm():
    llm = Ollama(model="phi3", request_timeout=300.0)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    Settings.llm = llm
    Settings.embed_model = embed_model


def init_index(embed_model):
    reader = SimpleDirectoryReader("./docs")
    documents = reader.load_data()

    logging.info("index creating with `%d` documents", len(documents))

    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.create_collection("iollama")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # use this to set custom chunk size and splitting
    # https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=embed_model)

    return index


def init_query_engine(index):
    global query_engine

    # custome prompt template
    template = """
                Imagine you are an advanced AI sales bot named 'Anas' for business EcoFresh, specializing in eco-friendly and sustainable household products. Your goal is to provide helpful, accurate, and concise answers to customer inquiries, using up-to-date information about EcoFresh's products and sustainability initiatives.

                Here is some context related to the query:
                -----------------------------------------
                {context_str}
                -----------------------------------------
                Considering the above information, please respond to the following customer inquiry with detailed references to EcoFresh's product offerings, sustainability practices, or company values where appropriate:

                **Note:** If the inquiry includes greetings or casual conversation, acknowledge them briefly and then focus on providing a precise and relevant answer to the main question.

                Question: {query_str}

                Ensure your response is clear and easy to understand for all customers and have maximum 2 sentences.
                """

    qa_template = PromptTemplate(template)

    # build query engine with custom template
    # text_qa_template specifies custom template
    # similarity_top_k configure the retriever to return the top 3 most similar documents,
    # the default value of similarity_top_k is 2
    query_engine = index.as_query_engine(
        text_qa_template=qa_template, similarity_top_k=3)

    return query_engine


def chat(input_question, user):
    global query_engine

    response = query_engine.query(input_question)
    logging.info("got response from llm - %s", response)

    return response.response


def chat_cmd():
    global query_engine

    while True:
        input_question = input("Enter your question (or 'exit' to quit): ")
        if input_question.lower() == 'exit':
            break

        response = query_engine.query(input_question)
        logging.info("got response from llm - %s", response)


if __name__ == '__main__':
    init_llm()
    index = init_index(Settings.embed_model)
    init_query_engine(index)
    chat_cmd()
