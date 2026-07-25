import csv
import sys
import matplotlib.pyplot as plt


def write_error():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
</body>
</html>"""

    with open("output.html", "w") as f:
        f.write(html)


def load_data():
    data = []

    try:
        with open("data.csv", "r", newline="") as f:
            reader = csv.reader(f, skipinitialspace=True)

            # Skip header
            next(reader)

            for row in reader:
                data.append(row)
    except Exception:
        return None

    return data


def student_details(student_id, data):
    rows = []
    total = 0

    for row in data:
        if row[0] == student_id:
            rows.append(row)
            total += int(row[2])

    if len(rows) == 0:
        write_error()
        return

    html = """<!DOCTYPE html>
<html>
<head>
    <title>Student Details</title>
</head>
<body>
    <h1>Student Details</h1>

    <table border="2">
        <tr>
            <th>Student ID</th>
            <th>Course ID</th>
            <th>Marks</th>
        </tr>
"""

    for row in rows:
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
        </tr>
"""

    html += f"""
        <tr>
            <td colspan="2"><b>Total Marks</b></td>
            <td>{total}</td>
        </tr>
    </table>
</body>
</html>
"""

    with open("output.html", "w") as f:
        f.write(html)


def course_details(course_id, data):
    marks = []

    for row in data:
        if row[1] == course_id:
            marks.append(int(row[2].strip()))

    if len(marks) == 0:
        write_error()
        return

    average = sum(marks) / len(marks)
    maximum = max(marks)

    plt.figure(figsize=(6, 4))
    plt.hist(marks, bins=10, edgecolor="black")
    plt.title("Marks Distribution")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("histogram.png")
    plt.close()

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Course Details</title>
</head>
<body>

    <h1>Course Details</h1>

    <table border="1">
        <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
        </tr>

        <tr>
            <td>{average:.1f}</td>
            <td>{maximum}</td>
        </tr>
    </table>

    <br>

    <img src="histogram.png" alt="Histogram">

</body>
</html>
"""

    with open("output.html", "w") as f:
        f.write(html)


def main():

    if len(sys.argv) != 3:
        write_error()
        return

    option = sys.argv[1]
    value = sys.argv[2]

    data = load_data()

    if data is None:
        write_error()
        return
    if any(value in dat for dat in data) is False:
        write_error()
        return

    if option == "-s":
        student_details(value, data)

    elif option == "-c":
        course_details(value, data)

    else:
        write_error()


if __name__ == "__main__":
    main()
    
