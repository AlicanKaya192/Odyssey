def mask_log(lines, secrets):
    # Bos olmayanlari uzundan kisaya sirala, sonra her satirda degistir.
    pass


log = ["Login as admin", "Using token abc123XYZ", "Retry with abc123XYZ-backup", "Done"]
for line in mask_log(log, ["abc123XYZ", "", "abc123XYZ-backup"]):
    print(line)
