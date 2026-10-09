import re


def mask_emails(text):
    return re.sub(r"[\w.]+@([\w.]+)", r"***@\1", text)

print(mask_emails("Mail ada.l@example.com or alan@test.org now"))
