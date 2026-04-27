import streamlit as st
import pandas as pd

st.set_page_config(page_title="PM Performance System", layout="wide")

# -------------------------
# UI STYLE SIMPLE
# -------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
h1 {
    color: white;
    text-align: center;
}
.card {
    padding: 15px;
    background-color: #1e293b;
    border-radius: 10px;
    margin-bottom: 10px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("Performance Management System")

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
# INPUT SECTION
# -------------------------
st.subheader("Ingreso de datos")

col1, col2 = st.columns(2)

with col1:
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

    days_diff = st.number_input(
        "Días (positivo = antes, negativo = tarde)",
        key=f"d{i}"
    )

    tasks.append({
        "completed": completed,
        "priority": priority,
        "days_diff": days_diff
    })

st.markdown("---")

days_required = st.number_input("Días requeridos")
days_attended = st.number_input("Días asistidos")

# -------------------------
# ADD MEMBER
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

    st.success(f"Usuario {name} agregado correctamente a la tabla")

    # CARD VISUAL
    st.markdown(f"""
    <div class="card">
        <h4>{name} ({division})</h4>
        <p>Output: {round(output,2)}</p>
        <p>Attendance: {round(attendance,2)}</p>
        <p>Delivery: {round(delivery,2)}</p>
        <p><b>Performance: {round(performance,2)}</b></p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# TABLE OUTPUT
# -------------------------
st.subheader("Tabla general")

if len(st.session_state.data) > 0:
    df = pd.DataFrame(st.session_state.data)
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
