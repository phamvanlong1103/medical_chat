import os
import streamlit as st
from dotenv import load_dotenv

# Gọi hàm tạo chain từ file retrieval_qa.py
from chains.retrieval_qa import create_retrieval_qa_chain

# Load biến môi trường (nếu cần)
load_dotenv()
# openai_api_key = st.secrets.get("OPENAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    openai_api_key =  st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.error("Không tìm thấy OPENAI_API_KEY trong st.secrets hoặc biến môi trường!")
# else:
#     st.write("Đã lấy được OPENAI_API_KEY thành công.")
    
def main():
    st.title("🤖 Chatbot Y Tế AI - RAG")

    # Khởi tạo chain RAG
    qa_chain = create_retrieval_qa_chain(openai_api_key)

    # Giao diện: user nhập câu hỏi
    user_query = st.text_input("Nhập câu hỏi về sức khoẻ của bạn...")

    if st.button("Gửi câu hỏi"):
        if not user_query.strip():
            st.warning("Vui lòng nhập nội dung câu hỏi!")
        else:
            with st.spinner("Đang xử lý..."):
                result = qa_chain.run(user_query)
            st.markdown(f"**Câu trả lời:** {result}")
            st.info("Đây chỉ là khuyến nghị. Hãy gặp bác sĩ để được chẩn đoán chính xác.")

if __name__ == "__main__":
    main()
