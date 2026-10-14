"""Support messages of a fictional outdoor shop, with their categories (read-only).

TICKETS: customer messages with the category a support agent gave them.
LABELS: the five categories. Every message is written by hand for the
lessons; none of them comes from a real customer.
"""

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]

_TEXTS = {
    "shipping": [
        "My parcel should have arrived on Monday. Where is it?",
        "The tracking page has not changed for four days.",
        "Do you deliver to Switzerland?",
        "How long does express delivery take?",
        "The courier left my order at the wrong address.",
        "Can I change the delivery address after ordering?",
        "Why do I have to pay a shipping fee on a 30 euro order?",
        "My order says delivered but nothing is at my door.",
    ],
    "returns": [
        "How do I send back a jacket that is too small?",
        "Can I return boots I only tried on at home?",
        "Where do I get a return label?",
        "I want to return an outlet item, is that possible?",
        "Is there a deadline for returning a tent?",
        "Can I exchange the backpack for a bigger size?",
        "The gloves do not fit, can I send them back?",
        "Do I need the original box to return the stove?",
    ],
    "refunds": [
        "I returned my order two weeks ago and still have no money back.",
        "When will the refund reach my credit card?",
        "I paid with a gift card, how do I get my refund?",
        "Why was the shipping cost not refunded?",
        "The refund amount is lower than what I paid.",
        "You received my return, when do I get the money?",
        "Can the refund go to a different bank account?",
        "I was refunded twice for the same jacket.",
    ],
    "warranty": [
        "The zip of my tent broke after one year.",
        "A seam of my backpack is coming apart.",
        "The sole of my boots came off after three months.",
        "My headlamp stopped working, is it under warranty?",
        "How do I make a warranty claim?",
        "The tent pole snapped in light wind.",
        "Is wear on the straps covered by the warranty?",
        "The stove leaks gas, what should I do?",
    ],
    "payment": [
        "Can I pay in three instalments?",
        "My card was declined at checkout.",
        "Do you accept bank transfer?",
        "I was charged twice for one order.",
        "Can my company pay by invoice?",
        "The discount code does not work at checkout.",
        "Can I use two gift cards on one order?",
        "Why is there a pending charge on my card?",
    ],
}

TICKETS = []
for _i in range(8):
    for _label in LABELS:
        TICKETS.append({"id": len(TICKETS) + 1, "text": _TEXTS[_label][_i], "label": _label})
