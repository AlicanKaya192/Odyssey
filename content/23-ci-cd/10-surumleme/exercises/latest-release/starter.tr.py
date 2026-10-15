def latest_release(tags):
    # Gecerli etiketlerin parcalarini sayiya cevir, en buyugunu tut.
    pass


tags = ["v1.2.0", "v1.10.0", "nightly", "v1.9.3", "v2.0.0rc1", "v1.10"]
print(latest_release(tags))
print(latest_release(["docs", "v0.1.0-beta"]))
print(latest_release(["v0.9.12", "v0.10.0"]))
