
import streamlit as st
import pandas as pd
from io import StringIO
import random


async def initial():
    st.title("Olá, seja bem vindo!")
    st.divider()
    st.subheader("Clique no botão abaixo para começar!")

    if 'perguntas' not in st.session_state:
        st.session_state.perguntas = []

    btn = st.button("Iniciar")
    if btn:
        uploadfile()


def uploadfile():
    if "perguntas" is not st.session_state:
        st.session_state.perguntas = {}
    try:
        with st.form("insert-json-file-form"):
            st.write("Envie o questionário")
            uploaded_file = st.file_uploader("Escolher um arquivo", type=["json"])
            if uploaded_file is not None:
                df = pd.read_json(StringIO(uploaded_file.getvalue().decode("utf-8")))
            submitted = st.form_submit_button("Enviar")
            if submitted:
                st.session_state.perguntas = df.perguntas
                st.write(st.session_state.perguntas)
    except:
        st.write('Selecione um arquivo')


def main():
    # Initialize chat history
    prompt = ''
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "respostas" not in st.session_state:
        st.session_state.respostas = {}

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    for pergunta in st.session_state.perguntas:

        if pergunta["tipo"] == "aberta":
            with st.chat_message("assistant"):
                st.write(pergunta['texto'])

            while prompt := st.text_input("E ai?", key=[random.randint(1, 1000)]):
                st.stop()

            with st.chat_message("user"):
                st.markdown(prompt)

        elif pergunta["tipo"] == "multipla_escolha":
            options = []
            for option in pergunta["opcoes"]:
                options.append(option)
            with st.chat_message("assistant"):
                prompt = st.radio(pergunta['texto'], options=options, key=[random.randint(1, 1000)])
            if prompt or asyncio.sleep(100):
                with st.chat_message("user"):
                    st.markdown(prompt)

        else:
            with st.chat_message("assistant"):
                prompt = st.radio(pergunta['texto'], options=["Verdadeiro", "Falso"], key=[random.randint(1, 1000)])
            if prompt or asyncio.sleep(100):
                with st.chat_message("user"):
                    st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": pergunta['texto']})


if __name__ == '__main__':
    import asyncio

    uploadfile()
    main()
