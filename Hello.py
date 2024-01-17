import streamlit as st
import pandas as pd
from io import StringIO
import random


def main():
    st.title("Olá, seja bem vindo!")
    st.divider()
    st.subheader("Clique no botão abaixo para começar!")

    uploadfile()


def uploadfile():
    try:
        with st.form("insert-json-file-form"):
            st.write("Envie o questionário")
            uploaded_file = st.file_uploader("Escolher um arquivo", type=["json"])
            if uploaded_file is not None:
                df = pd.read_json(StringIO(uploaded_file.getvalue().decode("utf-8")))
            submitted = st.form_submit_button("Enviar")
            if submitted:
                st.session_state.perguntas = df.perguntas
        chatbot()
    except:
        st.write('Selecione um arquivo')


def question(question_number, index):
    if question_number >= 1:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        pergunta = st.session_state.perguntas[index]
        if pergunta["tipo"] == "aberta":
            with st.chat_message("assistant"):
                st.write(pergunta['texto'])

            user_input = st.chat_input("E ai?", key=f"user_input + {random.randint(1, 100)}")
            if user_input:
                with st.chat_message("user"):
                    st.write(user_input)

        elif pergunta["tipo"] == "multipla_escolha":
            options = []
            for option in pergunta["opcoes"]:
                options.append(option)

            with st.chat_message("assistant"):
                user_input = st.radio(pergunta['texto'], options=options, key=[random.randint(1, 1000)], index=None)
            if user_input:
                with st.chat_message("user"):
                    st.write(user_input)

        else:
            with st.chat_message("assistant"):
                user_input = st.radio(pergunta['texto'], options=["Verdadeiro", "Falso"], key=[random.randint(1, 1000)],
                                      index=None)
            if user_input:
                with st.chat_message("user"):
                    st.write(user_input)
        if user_input:
            st.session_state.respostas.append({pergunta["text"]: user_input})
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": pergunta['texto']})
            return question(question_number-1, index+1)
    else:
        st.write("Faça o download do seu questionário")
        df = pd.DataFrame(st.session_state.messages)
        json_file = df.to_json(orient="records")
        st.download_button("Clique aqui para baixar", data=json_file, file_name="questionario_respondido.json")


def chatbot():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "respostas" not in st.session_state:
        st.session_state.respostas = []

    if "perguntas" not in st.session_state:
        st.session_state.perguntas = {}

    question(len(st.session_state.perguntas), 0)


if __name__ == '__main__':
    main()
