def ransomware_alert(stats, min_writes, min_ratio):
    flagged = []
    for name, s in stats.items():
        if s["extensions_changed"] / s["files_written"] > min_ratio:
            flagged.append(name)
    return flagged

stats = {
    "backup.exe": {"files_written": 4000, "extensions_changed": 0},
    "unknown.exe": {"files_written": 3800, "extensions_changed": 3700},
    "renamer.exe": {"files_written": 300, "extensions_changed": 300},
    "sync.exe": {"files_written": 0, "extensions_changed": 0},
}
print(ransomware_alert(stats, 1000, 0.5))
print(ransomware_alert(stats, 100, 0.5))
