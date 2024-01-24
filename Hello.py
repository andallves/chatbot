import streamlit as st
import pandas as pd
from io import StringIO

score_per_question = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "respostas" not in st.session_state:
    st.session_state.respostas = []

if "perguntas" not in st.session_state:
    st.session_state.perguntas = {}

if "score" not in st.session_state:
    st.session_state.score = 0.0

if "answer" not in st.session_state:
    st.session_state.answer = ''

if "clicked" not in st.session_state:
    st.session_state.clicked = False


def main():
    st.title("Olá, seja bem vindo!")
    st.divider()
    st.subheader("Clique no botão abaixo para começar!")
    st.button("Iniciar", on_click=button_change)

    if st.session_state.clicked:
        do_upload_file()

    if not st.session_state.perguntas.empty:
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

        if pergunta["tipo"] == "aberta":
            with st.chat_message("assistant"):
                st.write(pergunta['texto'])

            user_input = st.chat_input("E ai?", key=f"user_input_{index}")
            st.session_state.answer = user_input
            if user_input:
                with st.chat_message("user"):
                    st.write(user_input)

        elif pergunta["tipo"] == "multipla_escolha":
            options = []
            for option in pergunta["opcoes"]:
                options.append(option)

            with st.chat_message("assistant"):
                user_input = st.radio(pergunta['texto'], options=options, key=f"user_input_{index}", index=None)
            st.session_state.answer = user_input
            if user_input:
                with st.chat_message("user"):
                    st.write(user_input)

        else:
            with st.chat_message("assistant"):
                user_input = st.radio(pergunta['texto'], options=["Verdadeiro", "Falso"], key=f"user_input_{index}",
                                      index=None)
            st.session_state.answer = user_input
            if user_input:
                with st.chat_message("user"):
                    st.write(user_input)

        if st.session_state.answer:
            is_correct = check_answer(pergunta["resposta_correta"], st.session_state.answer.capitalize())
            if is_correct:
                st.session_state.score += score_per_question

            st.session_state.respostas.append({pergunta["texto"]: st.session_state.answer})
            st.session_state.messages.append({"role": "user", "content": st.session_state.answer})
            st.session_state.messages.append({"role": "assistant", "content": pergunta["texto"]})
            return question(question_number - 1, index + 1)

    elif question_number == 0:
        st.subheader(f"Sua pontuação é: {st.session_state.score}")
        st.write("Faça o download do seu questionário")
        df = pd.DataFrame(st.session_state.messages)
        json_file = df.to_json(orient="records")
        st.download_button("Clique aqui para baixar", data=json_file, file_name="questionario_respondido.json")

    else:
        return


def clean_chatbot():
    st.session_state.messages = {}


def chatbot():
    number_of_questions = len(st.session_state.perguntas)
    question(number_of_questions, 0)


if __name__ == '__main__':
    main()
