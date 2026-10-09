from typing import Literal, get_args

Mode = Literal["read", "write", "append"]


def is_valid_mode(value: str) -> bool:
    return value in get_args(Mode)

print(is_valid_mode("write"), is_valid_mode("delete"))
