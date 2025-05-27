import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Симулация на сблъсък - CERN", layout="wide")

# --- SESSION STATE за навигация ---
if "step" not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# Заглавие и меню напред/назад
st.title("🔬 Симулация на сблъсък на частици - Образователен модул CERN")

st.write(f"### Стъпка {st.session_state.step} от 5")

col_nav = st.columns([1,1,1])
with col_nav[0]:
    if st.session_state.step > 1:
        st.button("⬅ Назад", on_click=prev_step)
with col_nav[2]:
    if st.session_state.step < 5:
        st.button("Напред ➡", on_click=next_step)

st.markdown("---")

# --- Стъпка 1: Въведение с анимация ---
if st.session_state.step == 1:
    st.header("👀 Какво е сблъсък на частици?")
    st.markdown("""
    В ЦЕРН ускорителите сблъскват частици с много високи скорости,  
    за да разберем структурата на материята и вселената.  
    Вижте кратка анимация, която показва как протоните се сблъскват в големия адронен колайдер (LHC).
    """)
    
    # Вграждане на YouTube видео (може да се смени с друго)
    st.video("https://www.youtube.com/watch?v=V68v-R6nwsE")
    
    st.markdown("""
    След като разгледахте анимацията, преминете напред, за да симулираме сблъсък сами.
    """)

# --- Стъпка 2: Въвеждане на параметри и симулация ---
elif st.session_state.step == 2:
    st.header("🧪 Задайте параметри и пуснете симулация")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.number_input("Маса на частица 1 (kg)", min_value=0.1, value=5.0, step=0.1)
        v1 = st.number_input("Скорост на частица 1 (m/s)", value=5.0, step=0.1)

    with col2:
        m2 = st.number_input("Маса на частица 2 (kg)", min_value=0.1, value=5.0, step=0.1)
        v2 = st.number_input("Скорост на частица 2 (m/s)", value=-3.0, step=0.1)

    if st.button("▶ Пусни симулацията"):

        # Изчисляване на скоростите след еластичен сблъсък
        v1_final = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
        v2_final = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2

        # Записваме в сесия за следващите стъпки
        st.session_state.m1 = m1
        st.session_state.v1 = v1
        st.session_state.m2 = m2
        st.session_state.v2 = v2
        st.session_state.v1_final = v1_final
        st.session_state.v2_final = v2_final
        st.success("Симулацията е готова! Премини към следващата стъпка.")
        st.session_state.step = 3
        st.experimental_rerun()

# --- Стъпка 3: Въвеждане на хипотеза ---
elif st.session_state.step == 3:
    st.header("🤔 Какво очакваш да се случи?")

    hypothesis = st.text_area("Въведи своята хипотеза за скоростите и енергията след сблъсъка:", height=150)
    if st.button("📤 Изпрати хипотезата"):
        if hypothesis.strip():
            # Записване в CSV файл
            file = "hypotheses.csv"
            df = pd.DataFrame([{
                "timestamp": datetime.now().isoformat(),
                "mass1": st.session_state.m1,
                "velocity1": st.session_state.v1,
                "mass2": st.session_state.m2,
                "velocity2": st.session_state.v2,
                "hypothesis": hypothesis
            }])
            if os.path.exists(file):
                df.to_csv(file, mode='a', index=False, header=False)
            else:
                df.to_csv(file, index=False)

            st.success("Хипотезата ти е записана успешно!")
            st.session_state.user_hypothesis = hypothesis
            st.session_state.step = 4
            st.experimental_rerun()
        else:
            st.warning("Моля, въведи текст в хипотезата.")

# --- Стъпка 4: Показване на резултати и сравнение ---
elif st.session_state.step == 4:
    st.header("📉 Резултати от сблъсъка")

    m1 = st.session_state.m1
    v1 = st.session_state.v1
    m2 = st.session_state.m2
    v2 = st.session_state.v2
    v1_final = st.session_state.v1_final
    v2_final = st.session_state.v2_final

    impulse_before = m1 * v1 + m2 * v2
    impulse_after = m1 * v1_final + m2 * v2_final
    energy_before = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
    energy_after = 0.5 * m1 * v1_final ** 2 + 0.5 * m2 * v2_final ** 2

    st.write(f"**Импулс преди сблъсъка:** {impulse_before:.2f} kg·m/s")
    st.write(f"**Импулс след сблъсъка:** {impulse_after:.2f} kg·m/s")
    st.write(f"**Кинетична енергия преди сблъсъка:** {energy_before:.2f} J")
    st.write(f"**Кинетична енергия след сблъсъка:** {energy_after:.2f} J")

    st.markdown("""
    ---  
    ### Въпроси за размисъл:

    - Запазва ли се импулсът?
    - Запазва ли се кинетичната енергия?
    - Какво би се случило ако масите се променят?
    - Какъв тип сблъсък наблюдаваме?
    """)

    if st.button("Напред към статистика"):
        st.session_state.step = 5
        st.experimental_rerun()

# --- Стъпка 5: Статистика с всички хипотези ---
elif st.session_state.step == 5:
    st.header("📊 Как са се справили други ученици?")

    file = "hypotheses.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        st.write(f"Общо записани хипотези: {len(df)}")
        st.dataframe(df.tail(10))
    else:
        st.info("Все още няма записани хипотези.")

    st.markdown("Можеш да се върнеш назад и да опиташ с нови стойности или хипотези.")

