import json
import streamlit as st
import pandas as pd
from io import StringIO


def input_json(file_json):
    return pd.read_json(StringIO(file_json.getvalue().decode("utf-8")))


def ask_a_question(question, index):
    if question['tipo'] == 'multipla_escolha':
        text = question['texto']
        options = question['opcoes']
        return st.radio(text, options, key=index)
    elif question['tipo'] == 'verdadeiro_falso':
        text = question['texto']
        options = ['Verdadeiro', 'Falso']
        return st.radio(text, options, key=index)
    else:
        return st.text_input(question['texto'], key=index)


def verify_answer(correct_answer, user_answer):
    return correct_answer.lower() == user_answer.lower()


def send_answer(question_answered, user_input):
    global score_per_question
    if len(st.session_state.questions) > 0:
        score_per_question = 100 / len(st.session_state.questions)

    st.session_state.answers.append({"pergunta": questionary["texto"], "resposta": user_input})
    is_correct = verify_answer(question_answered['resposta_correta'], user_input)
    st.session_state.score += score_per_question if is_correct else 0

    st.session_state.index += 1


if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "score" not in st.session_state:
    st.session_state.score = 0.0

if "index" not in st.session_state:
    st.session_state.index = 0

score_per_question = 1

st.title("Olá, seja bem vindo!", )
st.divider()

json_uploaded = st.file_uploader("Escolher um arquivo", type=["json"])

if json_uploaded is not None:
    all_questions = input_json(json_uploaded)

    questions_length = len(all_questions)
    if questions_length >= 0 and st.session_state.index < len(all_questions):
        questionary = all_questions["perguntas"][st.session_state.index]

        input_answer = ask_a_question(questionary, questionary["id"])
        if input_answer:
            st.button("Enviar", on_click=send_answer, args=(questionary, str(input_answer)))
        else:
            st.write("Após responder digite enter!")

    else:
        st.subheader(f"Sua pontuação é: {st.session_state.score}")
        st.write("Faça o download do seu questionário")
        file = json.dumps(st.session_state.answers, indent=2, ensure_ascii=False)

        st.session_state.index = 0

        st.download_button("Clique aqui para baixar", data=file, file_name="questionario_respondido.json")
else:
    st.session_state.index = 0
