def finish_time(job, needs, minutes):
    # Bekledigi islerin en gec bitenini bul, kendi suresini ekle.
    pass


needs = {"lint": [], "test": [], "build": ["lint", "test"], "deploy": ["build"]}
minutes = {"lint": 2, "test": 5, "build": 3, "deploy": 1}
for job in needs:
    print(job, finish_time(job, needs, minutes))
