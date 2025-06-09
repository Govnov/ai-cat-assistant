import streamlit as st
from openai import OpenAI
import os
import base64

# ===== Настройка страницы =====
st.set_page_config(page_title="Котоассистент", page_icon="🐱")

# ===== Загрузка гифок =====
def load_gif_base64(path):
    full_path = os.path.join(os.path.dirname(__file__), path)
    with open(full_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

cat_left = load_gif_base64("assets/cat_left.gif")
cat_right = load_gif_base64("assets/cat_right.gif")

# ===== CSS для котиков =====
st.markdown(f"""
    <style>
        .cat-left {{
            position: fixed;
            left: 0;
            top: 25%;
            width: 240px;
            z-index: 1000;
        }}
        .cat-right {{
            position: fixed;
            right: 0;
            top: 25%;
            width: 240px;
            z-index: 1000;
        }}
    </style>
    <img src="data:image/gif;base64,{cat_left}" class="cat-left">
    <img src="data:image/gif;base64,{cat_right}" class="cat-right">
""", unsafe_allow_html=True)

# ===== API-ключ из секрета =====
client = OpenAI(api_key=st.secrets["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"])

# ===== Заголовок =====
st.title("Привет, я ассистент-котик!")

# ===== История диалога =====
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Ты — дружелюбный ассистент-котик."}
    ]

# ===== Форма ввода =====
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ты:", placeholder="Напиши что-нибудь...")
    submitted = st.form_submit_button("Отправить")

# ===== Запрос к OpenAI =====
if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Котик думает..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ===== Вывод истории =====
for msg in st.session_state.messages[1:]:
    role = "Ты" if msg["role"] == "user" else "🤖"
    st.markdown(f"**{role}:** {msg['content']}")

# ===== Кнопка сброса =====
if st.button("🧹 Сбросить диалог"):
    st.session_state.messages = [
        {"role": "system", "content": "Ты — дружелюбный ассистент-котик."}
    ]
    st.rerun()
