import difflib


def suggest(word, options):
    # get_close_matches may give an empty list
    return None

commands = ["start", "stop", "status", "restart", "help"]
print(suggest("hlep", commands))
print(suggest("xyz", commands))
