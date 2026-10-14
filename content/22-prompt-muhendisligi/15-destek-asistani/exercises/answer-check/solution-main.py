import re

from shop_data import LABELS, ORDERS

DETECT = re.compile(r"ignore (all |the )?(previous|above) instructions"
                    r"|reveal .{0,20}prompt|you are now", re.I)
ORDER_ID = re.compile(r"ORD-\d{5}")
PROMISE = re.compile(r"\b(will (arrive|reach)|tomorrow|guarantee)", re.I)
ACTION = re.compile(r"\b(cancelled|refunded|changed)\b", re.I)


def answer_problems(text, facts):
    problems = []
    for date in re.findall(r"\d{4}-\d{2}-\d{2}", text):
        if date != facts.get("date"):
            problems.append("date")
    if PROMISE.search(text):
        problems.append("promise")
    if ACTION.search(text):
        problems.append("action")
    return problems


FACTS = {"order_id": "ORD-48213", "status": "shipped",
         "date": "2026-10-09"}
for text in ["It was shipped on 2026-10-09.",
             "It will arrive on 2026-10-12.",
             "I have cancelled it for you."]:
    print(answer_problems(text, FACTS))
