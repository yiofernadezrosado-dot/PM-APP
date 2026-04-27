import streamlit as st
import pandas as pd

st.title("Sistema de Evaluación de Rendimiento")

# -------------------------
# INIT STORAGE (CLAVE)
# -------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# -------------------------
# DELIVERY SCORE
# -------------------------
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
    elif days_diff <= -3:
        return 0.3
    else:
        return 0

priority_weights = {
    "Low": 0.8,
    "Medium": 1.0,
    "High": 1.2
}

# -------------------------
# INPUT MEMBER
# -------------------------
name = st.text_input("Nombre del miembro")

num_tasks = st.number_input("Número de tareas", min_value=1, step=1)

tasks = []

for i in range(int(num_tasks)):
    st.subheader(f"Tarea {i+1}")

    priority = st.selectbox(
        "Prioridad",
        ["Low", "Medium", "High"],
        key=f"p{i}"
    )

    days_diff = st.number_input(
        "Días (deadline actual - entrega)",
        key=f"d{i}"
    )

    tasks.append({
        "priority": priority,
        "days_diff": days_diff
    })

# -------------------------
# ATTENDANCE
# -------------------------
st.subheader("Asistencia")

days_required = st.number_input("Días requeridos", min_value=1)
days_attended = st.number_input("Días asistidos", min_value=0)

# -------------------------
# BUTTON ADD MEMBER
# -------------------------
if st.button("Agregar miembro"):

    # OUTPUT (simplificado)
    output = 1.0  # porque tareas registradas = completadas en este modelo simple

    # DELIVERY
    adjusted_scores = []
    for t in tasks:
        base = delivery_score(t["days_diff"])
        adjusted_scores.append(base * priority_weights[t["priority"]])

    delivery = sum(adjusted_scores) / len(adjusted_scores)

    # ATTENDANCE
    attendance = days_attended / days_required

    # PERFORMANCE
    performance = (
        0.35 * output +
        0.35 * delivery +
        0.30 * attendance
    )

    # SAVE DATA
    st.session_state.data.append({
        "Miembro": name,
        "Output": round(output, 2),
        "Attendance": round(attendance, 2),
        "Delivery": round(delivery, 2),
        "Performance": round(performance, 2)
    })
#
# -------------------------
# SHOW TABLE (PERSISTENT)
# -------------------------
st.subheader("Tabla de rendimiento")

if len(st.session_state.data) > 0:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)
else:
    st.write("Aún no hay datos.")
