def fix_order(findings):
    return [finding_id for finding_id, severity in sorted(findings)]

FINDINGS = [
    ["F-7", "low"],
    ["F-2", "critical"],
    ["F-5", "medium"],
    ["F-1", "high"],
    ["F-3", "critical"],
    ["F-9", "unknown"],
]
for finding_id in fix_order(FINDINGS):
    print(finding_id)
