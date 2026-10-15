def image_tags(image, ref, sha):
    tags = [f"{image}:{sha[:7]}"]
    if ref == "refs/heads/main":
        tags.append(f"{image}:latest")
    if ref.startswith("refs/tags/v"):
        version = ref.removeprefix("refs/tags/v")
        tags.append(f"{image}:{version}")
        if not any(char.isalpha() for char in version):
            major, minor, _ = version.split(".")
            tags.append(f"{image}:{major}.{minor}")
            tags.append(f"{image}:{major}")
    return tags


image = "ghcr.io/ada/shop"
sha = "9c1e4b7a2f80d3c5"
refs = ["refs/heads/main", "refs/heads/cart",
        "refs/tags/v2.3.1", "refs/tags/v3.0.0rc1"]
for ref in refs:
    print(ref)
    for tag in image_tags(image, ref, sha):
        print("  " + tag)
