import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Симулация на сблъсък - CERN", layout="wide")

# Инициализиране на session state за стъпките
if "step" not in st.session_state:
    st.session_state.step = 1

def next_step():
    if st.session_state.step < 5:
        st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

st.title("Симулация на сблъсък на частици - Образователен модул CERN")

# Навигация между стъпките
col1, col2, col3 = st.columns([1,6,1])
with col1:
    if st.session_state.step > 1:
        st.button("⬅ Назад", on_click=prev_step)
with col3:
    if st.session_state.step < 5:
        st.button("Напред ➡", on_click=next_step)

# --- Стъпка 1: Въведение с видео ---
if st.session_state.step == 1:
    st.header("👀 Какво е сблъсък на частици?")
    st.markdown("""
    В ЦЕРН ускорителите сблъскват частици с много високи скорости,  
    за да разберем структурата на материята и вселената.  
    Вижте кратка анимация, която показва как протоните се сблъскват в големия адронен колайдер (LHC).
    """)
    st.video("https://www.youtube.com/watch?v=Yq0zeWX49SM")
    st.markdown("""
Това приложение симулира сблъсък между две частици в една линия (X-оста).  
Можете да променяте масата и скоростта на частиците и да наблюдавате как това влияе на резултатите.
""")

# --- Стъпка 2: Въвеждане на параметри и анимация ---
elif st.session_state.step == 2:
    st.header("🧪 Пускаш сблъсък с твои стойности")

    col1, col2 = st.columns(2)
    with col1:
        m1 = st.number_input("Маса на частица 1 (kg)", min_value=0.1, value=5.0, step=0.1, key="m1")
        v1 = st.number_input("Скорост на частица 1 (m/s)", value=5.0, step=0.1, key="v1")
    with col2:
        m2 = st.number_input("Маса на частица 2 (kg)", min_value=0.1, value=5.0, step=0.1, key="m2")
        v2 = st.number_input("Скорост на частица 2 (m/s)", value=-3.0, step=0.1, key="v2")

    # Изчисляваме крайни скорости при еластичен сблъсък
    v1_final = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
    v2_final = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2

    # Подготвяме траектории
    t = np.linspace(0, 2, 30)
    x1 = v1 * t
    x2 = 10 + v2 * t  # втората частица започва от позиция 10

    # Създаваме кадри за анимация
    frames = []
    for i in range(len(t)):
        frames.append(go.Frame(data=[
            go.Scatter3d(x=[x1[i]], y=[0], z=[0], mode='markers+text',
                         marker=dict(size=10, color='blue'),
                         text=["Частица 1"], textposition="top center"),
            go.Scatter3d(x=[x2[i]], y=[0], z=[0], mode='markers+text',
                         marker=dict(size=10, color='red'),
                         text=["Частица 2"], textposition="top center")
        ]))

    layout = go.Layout(
        scene=dict(
            xaxis=dict(range=[-10, 30], title='Позиция X'),
            yaxis=dict(range=[-5, 5], title='Y'),
            zaxis=dict(range=[-5, 5], title='Z'),
        ),
        title="3D Анимация на сблъсък",
        margin=dict(l=0, r=0, b=0, t=40),
        height=500,
        updatemenus=[dict(type="buttons", showactive=False,
                          buttons=[dict(label="▶ Пусни анимацията",
                                        method="animate",
                                        args=[None, {"frame": {"duration": 100, "redraw": True},
                                                     "fromcurrent": True}])])]

    )

    fig = go.Figure(
        data=[
            go.Scatter3d(x=[x1[0]], y=[0], z=[0], mode='markers', marker=dict(size=10, color='blue')),
            go.Scatter3d(x=[x2[0]], y=[0], z=[0], mode='markers', marker=dict(size=10, color='red'))
        ],
        layout=layout,
        frames=frames
    )

    st.plotly_chart(fig, use_container_width=True)

    # Запомняме резултатите за следващите стъпки
    st.session_state.v1_final = v1_final
    st.session_state.v2_final = v2_final
    st.session_state.impulse_before = m1 * v1 + m2 * v2
    st.session_state.impulse_after = m1 * v1_final + m2 * v2_final
    st.session_state.energy_before = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
    st.session_state.energy_after = 0.5 * m1 * v1_final ** 2 + 0.5 * m2 * v2_final ** 2

# --- Стъпка 3: Въвеждане на хипотеза ---
elif st.session_state.step == 3:
    st.header("🤔 Гадаеш какво ще стане")
    hypothesis = st.text_area("Какво очакваш да се случи със скоростите и енергията?", key="hypothesis")

    if st.button("Изпрати хипотезата"):
        if hypothesis.strip() == "":
            st.warning("Моля, въведи текст за хипотезата си.")
        else:
            # Записваме хипотезата (тук само в сесията, може да се съхрани и във файл/база)
            if "hypotheses" not in st.session_state:
                st.session_state.hypotheses = []
            st.session_state.hypotheses.append(hypothesis)
            st.success("Хипотезата ти е изпратена! Много добре, че мислиш активно!")
            # Автоматично преминаване към следващата стъпка
            next_step()

# --- Стъпка 4: Показване на резултати ---
elif st.session_state.step == 4:
    st.header("📉 Гледаш резултата и сравняваш")

    st.write(f"**Импулс преди сблъсъка:** {st.session_state.impulse_before:.2f} kg·m/s")
    st.write(f"**Импулс след сблъсъка:** {st.session_state.impulse_after:.2f} kg·m/s")
    st.write(f"**Кинетична енергия преди сблъсъка:** {st.session_state.energy_before:.2f} J")
    st.write(f"**Кинетична енергия след сблъсъка:** {st.session_state.energy_after:.2f} J")

    st.markdown("""
    ---  
    ### Въпроси за размисъл
    
    - Запазва ли се импулсът?  
    - Запазва ли се кинетичната енергия?  
    - Как масата и скоростта на частиците влияят на резултата?  
    - Какъв тип сблъсък е това (еластичен, нееластичен)?  
    """)

    st.markdown("Натисни „Напред“, за да видиш как са се справили другите ученици!")

# --- Стъпка 5: Статистика и сравнение ---
elif st.session_state.step == 5:
    st.header("📊 Виждаш как си се справил спрямо други")

    if "hypotheses" in st.session_state and len(st.session_state.hypotheses) > 0:
        st.write(f"Общо изпратени хипотези: {len(st.session_state.hypotheses)}")
        st.write("Примерни хипотези на други ученици:")
        for i, hyp in enumerate(st.session_state.hypotheses[-5:], 1):
            st.write(f"{i}. {hyp}")
    else:
        st.write("Все още няма изпратени хипотези.")

    st.markdown("Благодарим за участието в симулацията!")

