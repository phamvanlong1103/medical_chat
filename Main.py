import streamlit as st

# Sử dụng ChatOpenAI & OpenAIEmbeddings từ langchain_openai:
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Sử dụng FAISS từ langchain_community:
from langchain_community.vectorstores import FAISS

# Sử dụng các thành phần cốt lõi
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_core.prompts import PromptTemplate

# Hoặc tạm thời vẫn có thể import từ langchain, 
# nhưng sẽ bị cảnh báo trong phiên bản tương lai.

# Nhập PromptTemplate dạng "ChatPromptTemplate" (nếu cần):
from langchain.prompts.chat import (
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate, 
    ChatPromptTemplate
)
import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

from prompt.prompts import BASE_SYSTEM_PROMPT  # Từ file prompts.py

# 1. Chuẩn bị dữ liệu Document
docs = [
    Document(page_content="Bệnh cảm cúm thường gây ra triệu chứng sổ mũi, ho, đau đầu, mệt mỏi."),
    Document(page_content="Viêm phổi thường gây ra ho, khó thở, có khi sốt và đau ngực."),
]

# 2. Tạo Vector Store (FAISS)
embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = FAISS.from_documents(docs, embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 3. Cấu hình mô hình ChatOpenAI
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=openai_api_key
)

# 4. Định nghĩa biến my_prompt_template (CHÍNH LÀ CHỖ BỊ THIẾU)
my_prompt_template = """
Bạn là một trợ lý y tế AI.
Nội dung tài liệu hỗ trợ (context): {context}

Người dùng hỏi (question): {question}

Hãy đưa ra câu trả lời chi tiết. Sau đó, nhắc người dùng liên hệ bác sĩ nếu có bất kỳ dấu hiệu nghiêm trọng nào.
"""

prompt = PromptTemplate(
    template=my_prompt_template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={
        "prompt": prompt,
        # Mặc định chain "stuff" sẽ nhét tài liệu vào biến 'context' 
        # (Khớp với prompt template nêu trên)
        "document_variable_name": "context"
    }
)

# 5. Giao diện Streamlit
st.title("🤖 Chatbot Y Tế AI")

user_query = st.text_input("Nhập câu hỏi về sức khoẻ của bạn...")

if st.button("Gửi câu hỏi"):
    if user_query.strip() == "":
        st.warning("Vui lòng nhập nội dung câu hỏi!")
    else:
        with st.spinner("Đang xử lý..."):
            result = qa_chain.run(user_query)
        st.markdown(f"**Câu trả lời:** {result}")
        st.info("Đây chỉ là khuyến nghị. Hãy gặp bác sĩ để được chẩn đoán chính xác.")
