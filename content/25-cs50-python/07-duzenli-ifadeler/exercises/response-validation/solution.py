import validators

email = input("Email: ").strip()

if validators.email(email):
    print("Valid")
else:
    print("Invalid")
