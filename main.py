import streamlit as st
import datetime

st.set_page_config(page_title="Akylman Messenger", layout="centered")

# Функция для создания общего хранилища для ВСЕХ пользователей
@st.cache_resource
def get_global_messages():
    return []

# Получаем ссылку на этот общий список
all_messages = get_global_messages()

st.title("💬 Наш Мессенджер")

# Отображение сообщений из общего списка
chat_container = st.container(height=400)
with chat_container:
    for msg in all_messages:
        with st.chat_message(msg["role"]):
            st.write(f"**{msg['user']}** [{msg['time']}]: {msg['text']}")

# Поле ввода
if prompt := st.chat_input("Введите сообщение..."):
    now = datetime.datetime.now().strftime("%H:%M")
    # Добавляем в ОБЩИЙ список
    new_msg = {"role": "user", "user": "User_Shared", "time": now, "text": prompt}
    all_messages.append(new_msg)
    
    st.rerun()

# Кнопка обновления (Streamlit не обновляет чат сам, пока кто-то не нажмет кнопку или не напишет)
if st.button("Обновить чат"):
    st.rerun()
