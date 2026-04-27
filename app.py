import streamlit as st
import pandas as pd

st.set_page_config(page_title="PM Performance System", layout="wide")

# -------------------------
# STYLE (ANIMATED TITLE)
# -------------------------
st.markdown("""
<style>
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #3b82f6, #22c55e, #f97316);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glow 3s infinite alternate;
}

@keyframes glow {
    from {filter: brightness(1);}
    to {filter: brightness(1.5);}
}

.card {
    padding: 15px;
    background-color: #111827;
    border-radius: 12px;
    color: white;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>Performance Management System</div>", unsafe_allow_html=True)

# -------------------------
# STORAGE
# -------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# -------------------------
# CONFIG
# -------------------------
divisions = ["PES", "Astrobiology", "Robotics", "Design", "Software"]

priority_weights = {
    "Low": 0.8,
    "Medium": 1.0,
    "High": 1.2
}

def delivery_score(days_diff):
    if days_diff >= 2:
        return 1.2
    elif days_diff == 1:
        return 1.1
    elif days_diff == 0:
        return 1.0
    elif days_diff == -1:
        return 0.8
    elif days_diff == -2:
        return 0.6
    else:
        return 0.3

# -------------------------
# LEGEND / EXPLANATION
# -------------------------
with st.expander("Cómo funciona el sistema (Importante)"):
    st.write("""
    ### Sistema de fechas

    El sistema compara automáticamente:

    - Deadline original (fecha límite)
    - Fecha de entrega real

    Luego calcula:

    **Días = Deadline - Entrega**

    ### Interpretación:
    - Positivo → entregó antes
    - 0 → a tiempo
    - Negativo → tarde

    ### Ejemplo:
    - 2 → 2 días antes
    - -3 → 3 días tarde
    """)

# -------------------------
# INPUT
# -------------------------
st.subheader("Ingreso de datos")

name = st.text_input("Nombre del miembro")
division = st.selectbox("División", divisions)

num_tasks = st.number_input("Número de tareas", min_value=1, step=1)

tasks = []

st.markdown("---")
st.write("### Tareas")

for i in range(int(num_tasks)):

    st.markdown(f"**Tarea {i+1}**")

    completed = st.selectbox(
        "¿Tarea completada?",
        ["Sí", "No"],
        key=f"c{i}"
    )

    priority = st.selectbox(
        "Prioridad",
        ["Low", "Medium", "High"],
        key=f"p{i}"
    )

    st.markdown("#### Fechas")

    col1, col2 = st.columns(2)

    with col1:
        deadline = st.date_input(
            "Deadline original",
            key=f"dl{i}",
            help="Fecha límite oficial de la tarea"
        )

    with col2:
        delivery = st.date_input(
            "Fecha de entrega",
            key=f"dv{i}",
            help="Fecha en la que se entregó la tarea"
        )

    days_diff = (deadline - delivery).days

    st.info(f"Diferencia automática de días: {days_diff}")

    tasks.append({
        "completed": completed,
        "priority": priority,
        "days_diff": days_diff
    })

st.markdown("---")

days_required = st.number_input("Días requeridos")
days_attended = st.number_input("Días asistidos")

# -------------------------
# CALCULATE
# -------------------------
if st.button("Agregar miembro"):

    completed_tasks = sum(1 for t in tasks if t["completed"] == "Sí")
    output = completed_tasks / len(tasks)

    adjusted_scores = []

    for t in tasks:
        base = delivery_score(t["days_diff"])
        adjusted_scores.append(base * priority_weights[t["priority"]])

    delivery = sum(adjusted_scores) / len(adjusted_scores)
    attendance = days_attended / days_required

    performance = (
        0.35 * output +
        0.35 * delivery +
        0.30 * attendance
    )

    st.session_state.data.append({
        "Nombre": name,
        "División": division,
        "Output": round(output, 2),
        "Attendance": round(attendance, 2),
        "Delivery": round(delivery, 2),
        "Performance": round(performance, 2)
    })

    st.success("Miembro agregado correctamente")

    # VISUAL DASHBOARD
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Output", round(output, 2))
    col2.metric("Attendance", round(attendance, 2))
    col3.metric("Delivery", round(delivery, 2))
    col4.metric("Performance", round(performance, 2))

    st.markdown(f"""
    <div class="card">
        <h3>{name} - {division}</h3>
        <p>Registro añadido correctamente al sistema</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# TABLE
# -------------------------
st.subheader("Tabla general")

if len(st.session_state.data) > 0:

    df = pd.DataFrame(st.session_state.data)

    df.columns = [
        "Nombre",
        "División",
        "Output (Productividad)",
        "Attendance (Asistencia)",
        "Delivery (Tiempo)",
        "Performance (Final)"
    ]

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Descargar Excel (CSV)",
        csv,
        "performance_data.csv",
        "text/csv"
    )

else:
    st.write("No hay datos aún")