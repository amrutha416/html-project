from flask import Flask, request, render_template
import csv
import os

app = Flask(__name__)

# ✅ FIXED PATH (will work in any laptop)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "..", "data", "registrations.csv")

HEADERS = ["Name", "Roll", "Email", "Mobile", "Gender", "College", "Year", "Event", "Group", "Transaction"]


# ✅ Create CSV if not exists (adds heading)
def ensure_csv():
    if not os.path.exists(CSV_FILE):
        os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


@app.route("/")
def home():
    return "Backend running ✅ Use /view to display data"


# ✅ FORM SUBMISSION
@app.route("/submit", methods=["POST"])
def submit():
    ensure_csv()

    name = request.form.get("name", "").strip()
    roll = request.form.get("roll", "").strip()
    email = request.form.get("email", "").strip()
    mobile = request.form.get("mobile", "").strip()
    gender = request.form.get("gender", "").strip()
    college = request.form.get("college", "").strip()
    year = request.form.get("year", "").strip()
    event = request.form.get("event", "").strip()
    group = request.form.get("group", "").strip()
    transaction = request.form.get("transaction", "").strip()

    # ✅ default group for non-TechTalk
    if event != "Tech Talk":
        group = "None"

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, roll, email, mobile, gender, college, year, event, group, transaction])

    return "Form submitted successfully ✅ <br><a href='/view'>View Data</a>"


# ✅ VIEW + SEARCH + GROUPING
@app.route("/view")
def view():
    ensure_csv()

    search = request.args.get("search", "").strip().lower()

    normal_rows = []
    tech_talk_groups = {}

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # ✅ Clean blank group
            if not row.get("Group"):
                row["Group"] = "None"

            # ✅ SEARCH FILTER
            if search:
                combined = (
                    row["Name"] + row["Roll"] + row["Email"] + row["Mobile"] +
                    row["Gender"] + row["College"] + row["Year"] + row["Event"] +
                    row["Group"] + row["Transaction"]
                ).lower()

                if search not in combined:
                    continue

            # ✅ GROUPING
            if row["Event"] == "Tech Talk":
                grp = row["Group"]
                tech_talk_groups.setdefault(grp, []).append(row)
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
