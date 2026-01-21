from flask import Flask, request, render_template
import csv

app = Flask(__name__)

CSV_FILE = "../data/registrations.csv"

@app.route("/")
def home():
    return "Backend running. Use /submit for form and /view to display data."

# ---------- FORM SUBMISSION ----------
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    roll = request.form.get("roll")
    email = request.form.get("email")
    mobile = request.form.get("mobile")
    gender = request.form.get("gender")
    college = request.form.get("college")
    year = request.form.get("year")
    event = request.form.get("event")
    group = request.form.get("group")
    transaction = request.form.get("transaction")
    if event != "Tech Talk":
        group = "None"
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            name,
            roll,
            email,
            mobile,
            gender,
            college,
            year,
            event,
            group,
            transaction
        ])

    return "Form submitted successfully!"

# ---------- DISPLAY + SEARCH + GROUP ----------
@app.route("/view")
def view():
    search = request.args.get("search", "").strip().lower()

    normal_rows = []
    tech_talk_groups = {}

    with open(CSV_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # 🔍 SEARCH FIX: search across ALL fields safely
            combined = " ".join(row.values()).lower()

            # If search text exists and doesn't match, skip
            if search and search not in combined:
                continue

            # Grouping logic
            if row.get("Event") == "Tech Talk":
                group = row.get("Group")
                if group not in tech_talk_groups:
                    tech_talk_groups[group] = []
                tech_talk_groups[group].append(row)
            else:
                normal_rows.append(row)

    return render_template(
        "view.html",
        normal_rows=normal_rows,
        tech_talk_groups=tech_talk_groups,
        search=search
    )

if __name__ == "__main__":
    app.run(debug=True)
