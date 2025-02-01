from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_core.prompts import PromptTemplate
from data.docs_data import docs

from prompt.prompts import BASE_SYSTEM_PROMPT  # Lấy system prompt nếu cần

def create_retrieval_qa_chain(openai_api_key: str):
    """Khởi tạo chain RetrievalQA với FAISS vectorstore và prompt tuỳ chỉnh."""
    embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # 3) Cấu hình mô hình ChatOpenAI
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=openai_api_key
    )

    # 4) Tạo prompt template
    my_prompt_template = """
    Bạn là một trợ lý y tế AI.
    Nội dung tài liệu hỗ trợ (context): {context}

    Người dùng hỏi (question): {question}

    Hãy đưa ra câu trả lời chi tiết. 
    Sau đó, nhắc người dùng liên hệ bác sĩ nếu có bất kỳ dấu hiệu nghiêm trọng nào.
    """
    prompt = PromptTemplate(
        template=my_prompt_template,
        input_variables=["context", "question"]
    )

    # 5) Tạo chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={
            "prompt": prompt,
            "document_variable_name": "context"
        }
    )

    return qa_chain
