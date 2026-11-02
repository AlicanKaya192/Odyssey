def abac_allow(subject, resource, action, hour):
    same_dept = subject["dept"] == resource["dept"]
    if subject["role"] == "doctor":
        return same_dept
    if subject["role"] == "nurse":
        return same_dept and action == "read" and 7 <= hour < 19
    return False

nurse = {"role": "nurse", "dept": "cardiology", "mfa": True}
doctor = {"role": "doctor", "dept": "cardiology", "mfa": False}
normal = {"dept": "cardiology", "sensitivity": "normal"}
high = {"dept": "cardiology", "sensitivity": "high"}
print(abac_allow(nurse, normal, "read", 10), abac_allow(nurse, high, "read", 10))
print(abac_allow(doctor, normal, "write", 2), abac_allow(doctor, high, "read", 10))
