def missing_fields(plan, required):
    return [name for name in required if not plan.get(name)]

PLAN = {
    "written_permission": False,
    "signed_by": "Eve",
    "scope": ["10.20.0.0/24"],
    "window": [],
}
NEEDED = ["written_permission", "signed_by", "scope",
          "window", "emergency_contact"]
for name in missing_fields(PLAN, NEEDED):
    print(name)
