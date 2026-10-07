lines = ["alpha", "beta", "gamma"]
with open("/app/output.txt", "w") as handle:
    handle.write("\n".join(lines))
print("saved", len(lines), "lines as", __import__("getpass").getuser())
