import json

names = {1: "Ada", 2: "Alan", 3: "Grace"}
scores = {1: [90, 85], 2: [70, 95], 3: [88, 92]}
tags = {"python", "json", "files"}

print(json.loads(json.dumps(names)))

students = []
for student_id in sorted(names):
    marks = scores[student_id]
    students.append({
        "id": student_id,
        "name": names[student_id],
        "average": sum(marks) // len(marks),
    })
report = {"tags": sorted(tags), "students": students}

with open("report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=2)

with open("report.json", encoding="utf-8") as file:
    back = json.load(file)

print(back["tags"])
for student in back["students"]:
    print(student["id"], student["name"], student["average"])
print(type(back["students"][0]["id"]))
