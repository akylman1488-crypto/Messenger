import streamlit as st
import datetime

st.set_page_config(page_title="Akylman Private Messenger", layout="wide")

# Общее хранилище для ВСЕХ сообщений (в будущем заменим на БД)
@st.cache_resource
def get_db():
    return [] # Список словарей: {"from": ..., "to": ..., "text": ..., "time": ...}

db = get_db()

# 1. Авторизация (кто ты?)
my_name = st.sidebar.text_input("Твое имя (Логин):", value="User1")

# 2. Список доступных чатов (350 человек)
# Для примера создадим список из нескольких имен
all_users = ["User1", "User2", "Admin", "Cousin", "Friend_7th_Grade"]
chat_with = st.sidebar.selectbox("С кем переписываться?", [u for u in all_users if u != my_name])

st.title(f"Чат: {my_name} ↔️ {chat_with}")

# 3. Фильтрация сообщений для конкретного диалога
current_chat_messages = [
    msg for msg in db 
    if (msg["from"] == my_name and msg["to"] == chat_with) or 
       (msg["from"] == chat_with and msg["to"] == my_name)
]

# 4. Отображение чата
chat_container = st.container(height=400)
with chat_container:
    for msg in current_chat_messages:
        align = "user" if msg["from"] == my_name else "assistant"
        with st.chat_message(align):
            st.write(f"**{msg['from']}**: {msg['text']} *({msg['time']})*")

# 5. Отправка сообщения
if prompt := st.chat_input(f"Написать {chat_with}..."):
    now = datetime.datetime.now().strftime("%H:%M")
    new_msg = {
        "from": my_name,
        "to": chat_with,
        "text": prompt,
        "time": now
    }
    db.append(new_msg)
    st.rerun()

if st.sidebar.button("Обновить сообщения"):
    st.rerun()
