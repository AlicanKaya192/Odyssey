def rotate(sessions, old_id, new_id):
    result = dict(sessions)
    if old_id in result:
        result[new_id] = result.pop(old_id)
    return result

sessions = {"old123": "ada", "x9": "bob"}
after = rotate(sessions, "old123", "new456")
print(sorted(after.items()))
print(rotate(sessions, "missing", "zzz") == sessions)
