def approve(payment, approver):
    if approver == payment["created_by"]:
        return "denied"
    if approver in payment["approvals"]:
        return "duplicate"
    payment["approvals"].append(approver)
    needed = 2 if payment["amount"] >= 10000 else 1
    if len(payment["approvals"]) >= needed:
        return "approved"
    return "pending"

payment = {"amount": 25000, "created_by": "ada", "approvals": []}
for approver in ["ada", "alan", "alan", "grace"]:
    print(approver, approve(payment, approver))
small = {"amount": 900, "created_by": "ada", "approvals": []}
print("small", approve(small, "grace"))
