import streamlit as st
import openai
import os
import base64

# ========== НАСТРОЙКА СТРАНИЦЫ ==========
st.set_page_config(page_title="Котик-Ассистент", page_icon="🐱")

# ========== ФУНКЦИЯ ЗАГРУЗКИ ГИФОК ==========
def load_gif_base64(path):
    full_path = os.path.join(os.path.dirname(__file__), path)
    with open(full_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

cat_left = load_gif_base64("assets/cat_left.gif")
cat_right = load_gif_base64("assets/cat_right.gif")

# ========== КОТИКИ СЛЕВА И СПРАВА ==========
st.markdown(f"""
    <style>
        .cat-left {{
            position: fixed;
            left: 0;
            top: 30%;
            width: 300px;
            z-index: 1000;
        }}
        .cat-right {{
            position: fixed;
            right: 0;
            top: 30%;
            width: 300px;
            z-index: 1000;
        }}
    </style>
    <img src="data:image/gif;base64,{cat_left}" class="cat-left">
    <img src="data:image/gif;base64,{cat_right}" class="cat-right">
""", unsafe_allow_html=True)

# ========== OPENAI API-КЛЮЧ ==========
openai.api_key = "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"  # ⬅️ ВСТАВЬ СЮДА СВОЙ OpenAI API ключ

# ========== ЗАГОЛОВОК ==========
st.title("Привет, я ассистент-котик!")

# ========== ИНИЦИАЛИЗАЦИЯ ПАМЯТИ ==========
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Ты — дружелюбный ассистент-котик."}]

# ========== ФОРМА ДЛЯ ВВОДА ==========
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ты:", placeholder="Напиши что-нибудь...")
    submitted = st.form_submit_button("Отправить")

# ========== ОБРАБОТКА ОТВЕТА ==========
if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Котик думает..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ========== ВЫВОД ИСТОРИИ ==========
for msg in st.session_state.messages[1:]:
    role = "Ты" if msg["role"] == "user" else "🤖"
    st.markdown(f"**{role}:** {msg['content']}")

# ========== КНОПКА СБРОСА ==========
if st.button("🧹 Сбросить диалог"):
    st.session_state.messages = [{"role": "system", "content": "Ты — дружелюбный ассистент-котик."}]
    st.rerun()

