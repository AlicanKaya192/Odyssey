def approve(payment, approver):
    payment["approvals"].append(approver)
    return "approved"

payment = {"amount": 25000, "created_by": "ada", "approvals": []}
for approver in ["ada", "alan", "alan", "grace"]:
    print(approver, approve(payment, approver))
small = {"amount": 900, "created_by": "ada", "approvals": []}
print("small", approve(small, "grace"))
