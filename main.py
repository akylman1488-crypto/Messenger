import streamlit as st
import datetime

st.set_page_config(page_title="Akylman Messenger", layout="wide")

@st.cache_resource
def get_db():
    return []

db = get_db()

# Настройки в сайдбаре
st.sidebar.title("Аккаунт")
my_name = st.sidebar.text_input("Ваше имя:", value="User1")
all_users = ["Admin", "User1", "User2", "Cousin", "Friend"]
chat_with = st.sidebar.selectbox("Собеседник:", [u for u in all_users if u != my_name])

st.title(f"Чат: {my_name} ↔️ {chat_with}")

# Фрагмент, который обновляется сам каждые 2 секунды
@st.fragment(run_every="2s")
def show_messages():
    # Фильтруем сообщения внутри фрагмента, чтобы всегда видеть свежие
    current_chat = [
        m for m in db 
        if (m["from"] == my_name and m["to"] == chat_with) or 
           (m["from"] == chat_with and m["to"] == my_name)
    ]
    
    with st.container(height=450):
        for msg in current_chat:
            role = "user" if msg["from"] == my_name else "assistant"
            with st.chat_message(role):
                st.write(f"**{msg['from']}**: {msg['text']}")
                st.caption(msg['time'])

# Вызываем фрагмент
show_messages()

# Поле ввода (вне фрагмента, чтобы не сбрасывалось)
if prompt := st.chat_input("Напишите что-нибудь..."):
    now = datetime.datetime.now().strftime("%H:%M")
    db.append({
        "from": my_name,
        "to": chat_with,
        "text": prompt,
        "time": now
    })
    # Принудительно обновляем всё после отправки, чтобы сообщение появилось сразу
    st.rerun()
