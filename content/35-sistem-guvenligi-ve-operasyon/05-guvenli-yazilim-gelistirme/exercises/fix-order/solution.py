RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def fix_order(findings):
    ordered = sorted(findings, key=lambda f: (RANK.get(f[1], 4), f[0]))
    return [finding_id for finding_id, severity in ordered]

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
