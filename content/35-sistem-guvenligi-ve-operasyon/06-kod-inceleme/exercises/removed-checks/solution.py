def removed_checks(diff, keywords):
    found = []
    for line in diff.splitlines():
        if not line.startswith("-") or line.startswith("---"):
            continue
        text = line[1:].strip()
        if any(word in text for word in keywords):
            found.append(text)
    return found

DIFF = """--- a/app.py
+++ b/app.py
@@ -1,6 +1,5 @@
 def save(user, data):
-    check_owner(user, data)
-    verify_token(user)
-    print("saving")
+    print("saving now")
     store(data)
"""
for line in removed_checks(DIFF, ["check", "verify", "auth"]):
    print(line)
