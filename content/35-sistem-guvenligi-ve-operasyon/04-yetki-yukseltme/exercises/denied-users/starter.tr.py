def denied_users(lines, threshold):
    counts = {}
    for line in lines:
        fields = dict(part.split("=") for part in line.split()[2:])
        # reddedilenleri say
    return []

LOG = [
    "09:58 sudo user=ada result=ok cmd=update",
    "10:01 sudo user=bob result=denied cmd=passwd",
    "10:02 sudo user=bob result=denied cmd=restart",
    "10:02 sudo user=bob result=denied cmd=useradd",
    "10:05 sudo user=eve result=denied cmd=update",
    "10:06 sudo user=eve result=denied cmd=update",
]
print(denied_users(LOG, 3))
print(denied_users(LOG, 2))
