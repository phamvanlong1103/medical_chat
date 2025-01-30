from openai import OpenAI
import streamlit as st
from prompts import BASE_SYSTEM_PROMPT, CARDIO_SYSTEM_PROMPT, RESPIRATORY_SYSTEM_PROMPT

# Khởi tạo client OpenAI

# Hàm tạo phản hồi từ GPT
def generate_response(prompt):
    try:
        response = client.chat.completions.create(
           model="gpt-4o-mini",
        messages=[
        {"role": "system", "content": BASE_SYSTEM_PROMPT},   
        {"role": "user", "content": prompt}
    ],
    max_tokens=500,
    temperature=0.7
    )
        return response.choices[0].message.content
    except Exception as e:
        return f"Lỗi khi tạo phản hồi: {e}"

# Giao diện Streamlit
st.title("🤖 Chatbot Y Tế AI")
st.write("Xin chào! Tôi là trợ lý y tế AI. Hãy hỏi tôi bất kỳ câu hỏi nào về sức khỏe của bạn.")

# Lưu trữ lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhập câu hỏi từ người dùng
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Thêm câu hỏi vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tạo phản hồi từ GPT
    with st.spinner("Đang xử lý..."):
        response = generate_response(prompt)
    
    # Thêm phản hồi vào lịch sử
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)