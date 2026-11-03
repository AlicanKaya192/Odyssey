def release_blockers(checklist, required):
    return sorted(item for item in required if not checklist.get(item, False))

CHECKLIST = {
    "threat_model_reviewed": True,
    "security_tests_pass": False,
    "secrets_scan_clean": True,
}
REQUIRED = [
    "threat_model_reviewed",
    "security_tests_pass",
    "dependencies_scanned",
    "secrets_scan_clean",
]
for item in release_blockers(CHECKLIST, REQUIRED):
    print(item)
