import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Симулация на сблъсък - CERN", layout="wide")

st.title("Симулация на сблъсък на частици - Образователен модул CERN")

st.header("👀 Какво е сблъсък на частици?")
st.markdown("""
В ЦЕРН ускорителите сблъскват частици с много високи скорости,  
за да разберем структурата на материята и вселената.  
Вижте кратка анимация, която показва как протоните се сблъскват в големия адронен колайдер (LHC).
""")
st.video("https://www.youtube.com/watch?v=Yq0zeWX49SM")

st.markdown("---")

st.header("🧪 Пусни сблъсък с твои стойности")

col1, col2 = st.columns(2)
with col1:
    m1 = st.number_input("Маса на частица 1 (kg)", min_value=0.1, value=5.0, step=0.1)
    v1 = st.number_input("Скорост на частица 1 (m/s)", value=5.0, step=0.1)
with col2:
    m2 = st.number_input("Маса на частица 2 (kg)", min_value=0.1, value=5.0, step=0.1)
    v2 = st.number_input("Скорост на частица 2 (m/s)", value=-3.0, step=0.1)

collision_type = st.selectbox("Избери тип на сблъсъка:", ["Еластичен", "Нееластичен"])

# Изчисляване на резултати според типа сблъсък
if collision_type == "Еластичен":
    v1_final = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
    v2_final = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2
else:
    # Нееластичен - частиците се слепват
    v_final = (m1 * v1 + m2 * v2) / (m1 + m2)
    v1_final = v_final
    v2_final = v_final

# Подготвяне на траектории
t = np.linspace(0, 2, 30)
if collision_type == "Еластичен":
    x1 = v1 * t
    x2 = 10 + v2 * t
else:
    # За нееластичен сблъсък показваме движение на двете частици до сблъсък, после с обща скорост
    collision_time = 10 / (v1 - v2) if v1 != v2 else 1  # приближение за времето на сблъсък
    x1 = np.piecewise(t, [t < collision_time, t >= collision_time],
                      [lambda t: v1 * t, lambda t: v_final * t])
    x2 = np.piecewise(t, [t < collision_time, t >= collision_time],
                      [lambda t: 10 + v2 * t, lambda t: 10 + v_final * t])

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
    title=f"3D Анимация на {collision_type.lower()} сблъсък",
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

st.markdown("## 📉 Резултати от сблъсъка")

impulse_before = m1 * v1 + m2 * v2
impulse_after = m1 * v1_final + m2 * v2_final

energy_before = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
energy_after = 0.5 * m1 * v1_final ** 2 + 0.5 * m2 * v2_final ** 2

st.write(f"**Импулс преди сблъсъка:** {impulse_before:.2f} kg·m/s")
st.write(f"**Импулс след сблъсъка:** {impulse_after:.2f} kg·m/s")
st.write(f"**Кинетична енергия преди сблъсъка:** {energy_before:.2f} J")
st.write(f"**Кинетична енергия след сблъсъка:** {energy_after:.2f} J")

energy_loss = energy_before - energy_after
if collision_type == "Нееластичен":
    st.write(f"**Загуба на кинетична енергия:** {energy_loss:.2f} J (превръща се в топлина/деформация)")

st.markdown("---")

st.header("🤔 Въпроси за размисъл")

st.markdown("""
- Запазва ли се импулсът?  
- Запазва ли се кинетичната енергия?  
- Как се променят скоростите при различните типове сблъсъци?  
- Какво означава, ако кинетичната енергия намалява?  
""")

st.header("✍️ Въведи своя хипотеза за резултата от сблъсъка:")

hypothesis = st.text_area("Какво очакваш да се случи със скоростите и енергията?")

if st.button("Изпрати хипотезата"):
    if hypothesis.strip() == "":
        st.warning("Моля, въведи текст за хипотезата си.")
    else:
        if "hypotheses" not in st.session_state:
            st.session_state.hypotheses = []
        st.session_state.hypotheses.append(hypothesis)
        st.success("Хипотезата ти е изпратена! Много добре, че мислиш активно!")

        st.markdown("### Примерни хипотези на други ученици:")
        for i, hyp in enumerate(st.session_state.hypotheses[-5:], 1):
            st.write(f"{i}. {hyp}")
