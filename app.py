"""Интерфейс генератора котомемов на Streamlit.

Запуск из корня проекта:
    streamlit run app.py
"""

import streamlit as st

from config import MAX_TEXT_LENGTH
from src.cat_selector import CatSelector
from src.meme import make_meme
from src.text_model import TextModel


@st.cache_resource
def load_models():
    return TextModel(), CatSelector()


st.set_page_config(page_title="Генератор котомемов", page_icon="🐱")
st.title( "Генератор Шикотомемов")

text_model, selector = load_models()

phrase = st.text_area("Ваша фраза", max_chars=MAX_TEXT_LENGTH, height=100)

if st.button("Сгенерировать", type="primary"):
    phrase = " ".join(phrase.split())
    if not phrase:
        st.error("Фраза пустая.")
    else:
        prediction = text_model.predict(phrase)
        if not prediction.confident:
            st.info("Настроение определено неуверенно, показываем запасной вариант.")
        photo = selector.pick(prediction.label)
        png = make_meme(photo["path"], phrase)

        st.image(png)
        st.download_button("Скачать PNG", png, file_name="cat_meme.png", mime="image/png")
