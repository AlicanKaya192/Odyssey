LEVELS = ["public", "internal", "confidential", "restricted"]


def can_share(level, channel, channel_max):
    return LEVELS.index(level) <= LEVELS.index(channel_max[channel])

channel_max = {
    "website": "public",
    "team-chat": "internal",
    "encrypted-mail": "confidential",
}
print(can_share("internal", "team-chat", channel_max))
print(can_share("confidential", "team-chat", channel_max))
print(can_share("public", "file-site", channel_max))
print(can_share("secret", "website", channel_max))
