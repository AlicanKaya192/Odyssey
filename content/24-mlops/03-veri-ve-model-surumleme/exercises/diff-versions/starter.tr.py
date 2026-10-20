def diff_versions(old, new):
    # Satirlari kimlikle sozluge koy, sonra uc listeyi kur.
    pass


old = [{"id": "C1", "plan": "basic"}, {"id": "C2", "plan": "pro"}, {"id": "C3", "plan": "pro"}]
new = [{"id": "C3", "plan": "pro"}, {"id": "C2", "plan": "basic"}, {"id": "C4", "plan": "pro"}]
for key, ids in diff_versions(old, new).items():
    print(key, ids)
