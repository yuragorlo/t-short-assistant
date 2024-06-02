import os
from pathlib import Path
from textwrap import dedent
from langchain.agents import Tool
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool

@tool
def rag_faq_tool(query: str):
    """Find more relevant question-answer documents in vector db"""

    persist_directory = "./chroma_faq_db"
    collection_name = "FAQ"
    embed_model = OpenAIEmbeddings()

    if os.path.exists(persist_directory):
        print(f"load FAQ db from disk")
        db = Chroma(collection_name=collection_name,
                    persist_directory=persist_directory,
                    embedding_function=embed_model)
    else:
        print(f"make FAQ db")
        txt_content = Path('examples/FAQ.txt').read_text()
        qa_list = txt_content.split('\n')
        qa_chunks = [i + " " + j for i, j in zip(qa_list[::2], qa_list[1::2])]
        text_splitter = CharacterTextSplitter()
        splits = text_splitter.create_documents(qa_chunks)
        db = Chroma.from_documents(collection_name=collection_name,
                                   documents=splits,
                                   embedding=embed_model,
                                   persist_directory=persist_directory)
    docs = db.similarity_search_with_score(query=query, k=3)

    return docs

@tool
def rag_products_tool(query: str):
    """Find more relevant t-short blank documents in vector db"""

    persist_directory = "./chroma_product_db"
    collection_name = "products"
    embed_model = OpenAIEmbeddings()

    if os.path.exists(persist_directory):
        print(f"load products db from disk")
        db = Chroma(collection_name=collection_name,
                    persist_directory=persist_directory,
                    embedding_function=embed_model)
    else:
        print(f"make products db")
        txt_content = Path('examples/t_short_full_catalog.txt').read_text()
        qa_list = txt_content.split('\n\n')
        qa_chunks = [i + " " + j for i, j in zip(qa_list[::2], qa_list[1::2])]
        text_splitter = CharacterTextSplitter()
        splits = text_splitter.create_documents(qa_chunks)
        db = Chroma.from_documents(collection_name=collection_name,
                                   documents=splits,
                                   embedding=embed_model,
                                   persist_directory=persist_directory)
    docs = db.similarity_search_with_score(query=query, k=3)

    return docs


@tool
def send_support_requests(query: str):
    '''Sends a support requests based on the query.'''
    try:
        print(f"After user query: {query}, we send request to support team.")
        print(query)
        print("SENDING SUPPORT REQUESTS ...")
        return "Support request sent successfully."
    except Exception as e:
        return f"Support request was not sent successfully, error: {e}"


#
#
# result = rag_faq_tool("tell me which sizes do you have???")
# for r in result:
#     print("\n")
#     print(r[1])
#     print(r[0].page_content)


def get_tools(product_catalog):

    tools = [
        Tool(
            name="ProductSearch",
            func=rag_products_tool,
            description=dedent("""Useful for when you need answer the questions about 
            approximately product price. It contains t-shorts blanks, that company use like base
            and make custom pictures on it. It contain all other variants of t-shorts 
            (Styles, Genders, Colors, Sizes, Printing Options) with different prices per each one.
            Return list with 3 Document objects with t-shorts blanks and scores."""),
            # args_schema=product_input,

        ),
        Tool(
            name="FAQSearch",
            func=rag_faq_tool,
            description=dedent("""Useful for when you need more details 
            about product business possibilities, conditions and rules. 
            Contains most common questions and answers from other conversations, 
            where you can find more detailed information.
            Return list with 3 Document objects with question-answer pairs and scores."""),
            # args_schema=faq_input,
        ),
        Tool(
            name="SendSupportRequests",
            func=send_support_requests,
            description=dedent("""Useful to send support requests immediately, 
            if user ask you about it or you can't answer to the question using other tools, 
            or some unexpected situation."""),
        ),
    ]

    return tools


# from pydantic.v1 import BaseModel, Field
#
# class RagInput(BaseModel):
#     query: str = Field()
#     k: int
#     persist_directory: str
#     collection_name: str
#     source_file: str
#     chunks_separator: str
#
#
# @tool("RAG", return_direct=True, args_schema=RagInput)
# def rag_tool(query: str,
#              k: int,
#              persist_directory: str,
#              collection_name: str,
#              source_file: str,
#              chunks_separator: str) -> list:
#     """Find more relevant documents in vector db"""
#     embed_model = OpenAIEmbeddings()
#     if os.path.exists(persist_directory):
#         print(f"\nLoad DB from disk\n")
#         db = Chroma(collection_name=collection_name,
#                     persist_directory=persist_directory,
#                     embedding_function=embed_model)
#     else:
#         print(f"\nMake DB\n")
#         txt_content = Path(source_file).read_text()
#         qa_list = txt_content.split(chunks_separator)
#         qa_chunks = [i + " " + j for i, j in zip(qa_list[::2], qa_list[1::2])]
#         text_splitter = CharacterTextSplitter()
#         splits = text_splitter.create_documents(qa_chunks)
#         db = Chroma.from_documents(collection_name=collection_name,
#                                    documents=splits,
#                                    embedding=embed_model,
#                                    persist_directory=persist_directory)
#     docs = db.similarity_search_with_score(query=query, k=k)
#
#     return docs

   # faq_input = RagInput(
    #     k=3,
    #     persist_directory="./chroma_faq_db",
    #     collection_name="FAQ",
    #     source_file="examples/FAQ.txt",
    #     chunks_separator="\n",
    # )
    #
    # product_input = RagInput(
    #     k=3,
    #     persist_directory="./chroma_product_db",
    #     collection_name="products",
    #     source_file=product_catalog,
    #     chunks_separator="\n\n",
    # )
