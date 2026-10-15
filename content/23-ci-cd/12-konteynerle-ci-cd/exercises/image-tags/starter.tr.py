def image_tags(image, ref, sha):
    # Once SHA etiketi; sonra main ve surum etiketleri.
    pass


image = "ghcr.io/ada/shop"
sha = "9c1e4b7a2f80d3c5"
refs = ["refs/heads/main", "refs/heads/cart",
        "refs/tags/v2.3.1", "refs/tags/v3.0.0rc1"]
for ref in refs:
    print(ref)
    for tag in image_tags(image, ref, sha):
        print("  " + tag)
