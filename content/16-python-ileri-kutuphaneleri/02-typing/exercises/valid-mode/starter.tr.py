from typing import Literal, get_args

Mode = Literal["read", "write", "append"]


def is_valid_mode(value: str) -> bool:
    # get_args(Mode)
    return False

print(is_valid_mode("write"), is_valid_mode("delete"))
