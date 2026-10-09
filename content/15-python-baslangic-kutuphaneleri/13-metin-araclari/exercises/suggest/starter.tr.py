import difflib


def suggest(word, options):
    # get_close_matches bos liste verebilir
    return None

commands = ["start", "stop", "status", "restart", "help"]
print(suggest("hlep", commands))
print(suggest("xyz", commands))
