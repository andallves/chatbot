import streamlit as st
import pandas as pd
from io import StringIO
import random

score_per_question = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "respostas" not in st.session_state:
    st.session_state.respostas = []

if "perguntas" not in st.session_state:
    st.session_state.perguntas = {}

if "score" not in st.session_state:
    st.session_state.score = 0.0

if "clicked" not in st.session_state:
    st.session_state.clicked = False


def main():
    st.title("Olá, seja bem vindo!")
    st.divider()
    st.subheader("Clique no botão abaixo para começar!")
    st.button("Iniciar", on_click=button_change)

    if st.session_state.clicked:
        do_upload_file()

    if do_upload_file():
        chatbot()


def button_change():
    st.session_state.clicked = True


def do_upload_file():
    try:
        with st.form("insert-json-file-form"):
            st.write("Envie o questionário")
            uploaded_file = st.file_uploader("Escolher um arquivo", type=["json"])
            if uploaded_file is not None:
                df = pd.read_json(StringIO(uploaded_file.getvalue().decode("utf-8")))
            submitted = st.form_submit_button("Enviar")
            if submitted:
                st.session_state.perguntas = df.perguntas
                return True
    except:
        st.write('Selecione um arquivo')


def check_answer(correct_answer, input_answer):
    return correct_answer == input_answer


def question(question_number, index):
    if question_number >= 1:
        global score_per_question
        score_per_question = 100 / question_number
        pergunta = st.session_state.perguntas[index]

        user_input = None

        if pergunta["tipo"] == "aberta":
            with st.chat_message("assistant"):
                st.write(pergunta['texto'])

            user_input = st.chat_input("E ai?", key=f"user_input_{index}")
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
            is_correct = check_answer(pergunta["resposta_correta"], user_input)
            if is_correct:
                st.session_state.score += score_per_question

            st.session_state.respostas.append({pergunta["texto"]: user_input})
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": pergunta["texto"]})
            question(question_number-1, index+1)
    else:
        st.subheader(f"Sua pontuação é: {st.session_state.score}")
        st.write("Faça o download do seu questionário")
        df = pd.DataFrame(st.session_state.messages)
        json_file = df.to_json(orient="records")
        st.download_button("Clique aqui para baixar", data=json_file, file_name="questionario_respondido.json")


def chatbot():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question(len(st.session_state.perguntas), 0)


if __name__ == '__main__':
    main()

