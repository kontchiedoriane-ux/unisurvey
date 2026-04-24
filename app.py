from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ------------------ DATABASE ------------------
def init_db():
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    conn.close()

# ------------------ FORM PAGE ------------------
@app.route('/')
def form():
    return """
    <h1>🎓 UniSurvey - Sondage Étudiant</h1>
    <form method="post" action="/submit">

    Nom (optionnel): <input type="text" name="name"><br><br>

    Âge: <input type="number" name="age" required><br><br>

    Sexe:
    <select name="gender">
        <option>Masculin</option>
        <option>Féminin</option>
    </select><br><br>

    Filière: <input type="text" name="field" required><br><br>

    Niveau:
    <select name="level">
        <option>L1</option>
        <option>L2</option>
        <option>L3</option>
        <option>M1</option>
        <option>M2</option>
    </select><br><br>

    Moyenne: <input type="number" step="0.1" name="grade" required><br><br>

    Heures d'étude/jour: <input type="number" step="0.1" name="hours" required><br><br>

    Satisfaction (1 à 5):
    <input type="number" min="1" max="5" name="satisfaction" required><br><br>

    <button type="submit">Envoyer</button>
    </form>

    <br>
    <a href="/stats">Voir les statistiques</a>
    """

# ------------------ SUBMIT ------------------
@app.route('/submit', methods=['POST'])
def submit():
    data = (
        request.form['name'],
        request.form['age'],
        request.form['gender'],
        request.form['field'],
        request.form['level'],
        request.form['grade'],
        request.form['hours'],
        request.form['satisfaction']
    )

    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    c.execute("INSERT INTO students(name, age, gender, field, level, grade, hours, satisfaction) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

    return redirect(url_for('stats'))

# ------------------ STATS ------------------
@app.route('/stats')
def stats():
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()

    c.execute("SELECT AVG(grade), AVG(hours), AVG(satisfaction), COUNT(*) FROM students")
    avg_grade, avg_hours, avg_sat, count = c.fetchone()

    c.execute("SELECT name, age, gender, field, level, grade, hours, satisfaction FROM students")
    rows = c.fetchall()

    conn.close()

    table = ""
    for r in rows:
        table += f"<tr>{''.join(f'<td>{x}</td>' for x in r)}</tr>"

    return f"""
    <h1>📊 Résultats du sondage</h1>

    <h3>Statistiques générales</h3>
    <p>👨‍🎓 Nombre d'étudiants : {count}</p>
    <p>📘 Moyenne générale : {round(avg_grade,2) if avg_grade else 0}</p>
    <p>⏱️ Heures moyennes d'étude : {round(avg_hours,2) if avg_hours else 0}</p>
    <p>⭐ Satisfaction moyenne : {round(avg_sat,2) if avg_sat else 0}</p>

    <h3>Données collectées</h3>
    <table border="1">
        <tr>
            <th>Nom</th><th>Age</th><th>Sexe</th><th>Filière</th>
            <th>Niveau</th><th>Moyenne</th><th>Heures</th><th>Satisfaction</th>
        </tr>
        {table}
    </table>

    <br><a href="/">⬅ Retour</a>
    """

# ------------------ RUN ------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
