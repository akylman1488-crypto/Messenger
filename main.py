import streamlit as st
import datetime

st.set_page_config(page_title="Akylman Messenger", layout="centered")

# Инициализация истории сообщений в памяти сервера
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 Наш Мессенджер")

# Отображение сообщений
chat_container = st.container(height=400)
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(f"**{msg['user']}** [{msg['time']}]: {msg['text']}")

# Поле ввода
if prompt := st.chat_input("Введите сообщение..."):
    # Добавляем сообщение в историю
    now = datetime.datetime.now().strftime("%H:%M")
    new_msg = {"role": "user", "user": "User_1", "time": now, "text": prompt}
    
    st.session_state.messages.append(new_msg)
    
    # Перезагружаем интерфейс, чтобы сообщение появилось
    st.rerun()
