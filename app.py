import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('survey.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS students(
    name TEXT,
    age INTEGER,
    gender TEXT,
    field TEXT,
    level TEXT,
    grade REAL,
    hours REAL,
    satisfaction INTEGER
)''')
conn.commit()

st.title("🎓 UniSurvey - Sondage des étudiants")

with st.form("form"):
    name = st.text_input("Nom (optionnel)")
    age = st.number_input("Âge", min_value=15, max_value=50)
    gender = st.selectbox("Sexe", ["Masculin", "Féminin"])
    field = st.text_input("Filière")
    level = st.selectbox("Niveau", ["L1", "L2", "L3", "M1", "M2"])
    grade = st.number_input("Moyenne", min_value=0.0, max_value=20.0)
    hours = st.number_input("Heures d'étude / jour", min_value=0.0, max_value=24.0)
    satisfaction = st.slider("Satisfaction", 1, 5)

    submitted = st.form_submit_button("Envoyer")

    if submitted:
        c.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, age, gender, field, level, grade, hours, satisfaction))
        conn.commit()
        st.success("✅ Données enregistrées !")

st.header("📊 Statistiques")

df = pd.read_sql("SELECT * FROM students", conn)

if not df.empty:
    st.write("👨‍🎓 Nombre d'étudiants :", len(df))
    st.write("📘 Moyenne générale :", round(df['grade'].mean(), 2))
    st.write("⏱️ Heures moyennes :", round(df['hours'].mean(), 2))
    st.write("⭐ Satisfaction moyenne :", round(df['satisfaction'].mean(), 2))

    st.dataframe(df)
    st.bar_chart(df['grade'])

else:
    st.info("Aucune donnée pour le moment.")
