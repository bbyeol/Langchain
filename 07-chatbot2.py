import streamlit as st
from langchain_openai import ChatOpenAI  
import os
#from openai import OpenAI
#import streamlit as st
#from dotenv import load_dotenv

#load_dotenv()
#### 내 컴 내부의 env를 활용하여 로드해서 하는건데 퍼블리시 할려면 내env를 퍼블리시 하면 안되니까 chatbot2로 고치기

# Streamlit UI 설정
st.set_page_config(page_title="ChatOpenAI Demo", page_icon=":robot:")
st.header("ChatOpenAI Demo")


# 사이드바에 OpenAI API 키 입력 필드 생성, open ai key를 어디서 필요할지 모르니까 위쪽에서 이니셜라이즈.
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# ChatOpenAI 모델 초기화
chat = ChatOpenAI(temperature=0)


# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# 대화 히스토리 표시
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력 처리
#promp = st.chat_input("무엇을 도와드릴까요?")
#if prompt 
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in chat.stream(st.session_state.messages):
            full_response += (response.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 스크롤을 최하단으로 이동
st.empty()