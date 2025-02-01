import streamlit as st
from app import Chat


if "chat_instance" not in st.session_state:
    api_key = st.secrets["api_keys"]["my_api_key"]
    st.session_state.chat_instance = Chat(
        "accounts/fireworks/models/llama-v3p3-70b-instruct", api_key
    )


if "user_chat" not in st.session_state:
    st.session_state.user_chat = []

if "bot_chat" not in st.session_state:
    st.session_state.bot_chat = []


def generar_interfaz(nombre):
    st.header(f"{nombre}")

    user_input = st.text_input("Ingrese su consulta:")
    if user_input:
        st.session_state.user_chat.append(user_input)
        bot_response = st.session_state.chat_instance.run(
            user_input, st.session_state.bot_chat
        )
        st.session_state.bot_chat.append(bot_response)

    for i in range(len(st.session_state.user_chat)):
        st.markdown(f"**Usuario:** {st.session_state.user_chat[i]}")
        print(st.session_state.bot_chat[i]["choices"])
        st.markdown(f"**Asistente:** {st.session_state.bot_chat[i]['choices']}")


def main():
    st.title("Bienvenido a su asistente virtual")
    st.markdown("---")

    option = st.selectbox(
        "Seleccione una opción:", ["", "Asistente Vocacional", "Asistente Jurídico"]
    )

    if option == "Asistente Vocacional":
        generar_interfaz("Asistente Vocacional")

    elif option == "Asistente Jurídico":
        generar_interfaz("Asistente Jurídico")


if __name__ == "__main__":
    main()
