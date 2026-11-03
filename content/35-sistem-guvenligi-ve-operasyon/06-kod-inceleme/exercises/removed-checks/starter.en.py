def removed_checks(diff, keywords):
    found = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            found.append(line[1:].strip())
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
