import streamlit as st
import sqlite3
import datetime
from streamlit_cookies_manager import EncryptedCookieManager

# Настройка куки (для хранения сессии)
cookies = EncryptedCookieManager(password="secret_password_123")
if not cookies.ready():
    st.stop()

# --- РАБОТА С БАЗОЙ ДАННЫХ ---
def init_db():
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (sender TEXT, receiver TEXT, text TEXT, time TEXT)''')
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('messenger.db')
    users = [row[0] for row in conn.execute('SELECT username FROM users').fetchall()]
    conn.close()
    return users

init_db()

# --- ЛОГИКА ВХОДА ---
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = cookies.get("user")

# Окно регистрации/входа
if not st.session_state.logged_in_user:
    st.title("Добро пожаловать в Akylman Messenger")
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    
    with tab2:
        reg_user = st.text_input("Придумайте логин")
        reg_pass = st.text_input("Придумайте пароль", type="password")
        if st.button("Зарегистрироваться"):
            try:
                conn = sqlite3.connect('messenger.db')
                conn.execute('INSERT INTO users VALUES (?, ?)', (reg_user, reg_pass))
                conn.commit()
                st.success("Аккаунт создан! Теперь войдите.")
            except:
                st.error("Это имя уже занято.")
            finally:
                conn.close()

    with tab1:
        login_user = st.text_input("Логин")
        login_pass = st.text_input("Пароль", type="password")
        if st.button("Войти"):
            conn = sqlite3.connect('messenger.db')
            user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', 
                                (login_user, login_pass)).fetchone()
            if user:
                st.session_state.logged_in_user = login_user
                cookies["user"] = login_user
                cookies.save()
                st.rerun()
            else:
                st.error("Неверный логин или пароль")
            conn.close()
    st.stop()

# --- ИНТЕРФЕЙС МЕССЕНДЖЕРА ---
my_name = st.session_state.logged_in_user

# Выход из аккаунта
if st.sidebar.button("Выйти"):
    cookies.update({"user": ""})
    cookies.save()
    st.session_state.logged_in_user = None
    st.rerun()

# Список всех людей
all_users = get_all_users()
chat_with = st.sidebar.selectbox("Выберите чат:", [u for u in all_users if u != my_name])

st.title(f"Вы: {my_name} | Чат с: {chat_with}")

@st.fragment(run_every="2s")
def show_messages():
    conn = sqlite3.connect('messenger.db')
    messages = conn.execute('''SELECT sender, text, time FROM messages 
                               WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)''',
                            (my_name, chat_with, chat_with, my_name)).fetchall()
    conn.close()
    
    with st.container(height=400):
        for msg in messages:
            role = "user" if msg[0] == my_name else "assistant"
            with st.chat_message(role):
                st.write(f"**{msg[0]}**: {msg[1]}")
                st.caption(msg[2])

show_messages()

if prompt := st.chat_input("Сообщение..."):
    now = datetime.datetime.now().strftime("%H:%M")
    conn = sqlite3.connect('messenger.db')
    conn.execute('INSERT INTO messages VALUES (?, ?, ?, ?)', (my_name, chat_with, prompt, now))
    conn.commit()
    conn.close()
    st.rerun()

# В сайдбаре:
st.sidebar.markdown("---")
st.sidebar.subheader("Управление")

if st.sidebar.button("🗑️ Очистить текущий чат", use_container_width=True):
    with sqlite3.connect('messenger.db') as conn:
        cursor = conn.cursor()
        # Выполняем удаление
        cursor.execute('''DELETE FROM messages 
                          WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)''', 
                       (my_name, chat_with, chat_with, my_name))
        conn.commit()
    
    # Это критически важно: уведомляем Streamlit, что данные изменились
    st.toast(f"Чат с {chat_with} очищен")
    st.rerun()
