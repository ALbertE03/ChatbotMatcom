import streamlit as st
from streamlit_chat import message
from chat import Chat


if "chat_instance" not in st.session_state:
    api_key = st.secrets["api_keys"]["my_api_key"]
    st.session_state.chat_instance = Chat(
        "accounts/fireworks/models/llama-v3p3-70b-instruct", api_key
    )


if "user_chat" not in st.session_state:
    st.session_state.user_chat = []

if "bot_chat" not in st.session_state:
    st.session_state.bot_chat = []


def extract_content(bot_response):

    content = bot_response["choices"][0]["message"]["content"]
    return content


def generar_interfaz(nombre):
    st.header(f"{nombre}")

    chat_container = st.container()
    user_input = st.chat_input("Escribe tu mensaje aquí...")

    if user_input:
        st.session_state.user_chat.append(user_input)
        bot_response = st.session_state.chat_instance.run(
            user_input, st.session_state.bot_chat
        )
        st.session_state.bot_chat.append(bot_response)

    with chat_container:
        for i in range(len(st.session_state.user_chat)):
            message(st.session_state.user_chat[i], is_user=True, key=f"user_{i}")
            bot_content = extract_content(st.session_state.bot_chat[i])
            message(bot_content, is_user=False, key=f"bot_{i}")


def main():
    st.title("Bienvenido a su asistente virtual")
    st.markdown("---")

    option = st.radio(
        "Seleccione una opción:", ["Asistente Vocacional", "Asistente Jurídico"]
    )

    if option == "Asistente Vocacional":
        generar_interfaz("Asistente Vocacional")

    elif option == "Asistente Jurídico":
        generar_interfaz("Asistente Jurídico")


if __name__ == "__main__":
    main()
