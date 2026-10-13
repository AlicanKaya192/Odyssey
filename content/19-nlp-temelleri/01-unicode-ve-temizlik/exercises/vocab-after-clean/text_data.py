"""Sample text data for the NLP lessons.

Every call with the same arguments returns exactly the same texts on every
machine: the generator uses its own random.Random(seed) and never the global
random module.

    make_reviews(n, seed=7)   -> list of dicts: id, product, text, rating, label
    make_tickets(n, seed=11)  -> list of dicts: id, text, category, priority
    messy_reviews(n, seed=5)  -> the same reviews with web-page clutter
    write_reviews_csv(path, n, seed=7)
    write_tickets_csv(path, n, seed=11)

Review labels are "positive" (rating 4-5), "negative" (rating 1-2) and
"neutral" (rating 3). Ticket categories are billing, shipping, account,
technical and refund.
"""
import csv
import random

# ---------------------------------------------------------------- reviews

PRODUCTS = {
    "headphones": ["sound", "battery", "comfort", "noise cancelling", "bluetooth connection"],
    "coffee maker": ["coffee", "brewing time", "water tank", "cleaning", "noise"],
    "backpack": ["zipper", "straps", "pockets", "material", "size"],
    "phone case": ["grip", "fit", "buttons", "colour", "protection"],
    "desk lamp": ["light", "brightness", "switch", "cable", "base"],
    "sports watch": ["strap", "screen", "battery", "step counter", "weight"],
    "water bottle": ["lid", "insulation", "seal", "handle", "size"],
    "office chair": ["seat", "armrests", "wheels", "back support", "assembly"],
}

# "good" words take a booster ("very good"); "great" words stand alone.
GOOD_ADJ = ["good", "solid", "comfortable", "reliable", "sturdy", "nice", "quiet"]
GREAT_ADJ = ["great", "excellent", "perfect", "fantastic", "impressive"]
BAD_ADJ = ["bad", "weak", "flimsy", "poor", "uncomfortable", "loud", "fragile"]
AWFUL_ADJ = ["terrible", "awful", "useless", "disappointing"]
MID_ADJ = ["okay", "fine", "average", "acceptable", "decent"]
BOOST = ["really", "very", "super", "quite", "pretty", "extremely"]

POS_SENT = [
    "The {aspect} is {boost} {good}.",
    "The {aspect} is {great}.",
    "I love the {aspect}.",
    "{Aspect} works {boost} well.",
    "Totally worth the money.",
    "Would buy this {product} again.",
    "Arrived early and well packed.",
    "Five stars for the {aspect}.",
    "Exactly what I needed.",
    "My {relative} loves it too.",
    "Much better than my old {product}.",
]
NEG_SENT = [
    "The {aspect} is {boost} {bad}.",
    "The {aspect} is {awful}.",
    "I hate the {aspect}.",
    "{Aspect} stopped working after {days} days.",
    "Not worth the money.",
    "I would not buy this {product} again.",
    "Arrived late and the box was damaged.",
    "Returned it after a week.",
    "Waste of money.",
    "Customer service never answered.",
    "Worse than my old {product}.",
]
MID_SENT = [
    "The {aspect} is {mid}.",
    "It does the job.",
    "Nothing special about the {aspect}.",
    "{Aspect} is {mid} for the price.",
    "Overall, the {product} is {mid}.",
    "Delivery took {days} days.",
]
# Negated praise and negated complaint: bag-of-words models trip over these.
NEG_OF_GOOD = ["The {aspect} is not {good} at all.", "I can't say the {aspect} is {good}.",
               "Not {boost} {good}, to be honest."]
NEG_OF_BAD = ["The {aspect} is not {bad} at all.",
              "I expected the {aspect} to be {bad}, but no.",
              "Not {bad} for the price."]
# Sarcasm: positive words, negative meaning.
SARCASM = ["Great, the {aspect} broke on day {days}.", "Just perfect, the {aspect} is {bad} again.",
           "Wonderful, it stopped working after {days} days."]
RELATIVES = ["wife", "husband", "son", "daughter", "friend", "brother", "sister"]

TYPO_RATE = 0.03


def _typo(word, rng):
    if len(word) < 4 or not word.isalpha():
        return word
    i = rng.randrange(1, len(word) - 2)
    return word[:i] + word[i + 1] + word[i] + word[i + 2:]


def _fill(template, rng, product, aspects):
    aspect = rng.choice(aspects)
    text = template.format(
        aspect=aspect, Aspect=aspect.capitalize(), product=product,
        good=rng.choice(GOOD_ADJ), great=rng.choice(GREAT_ADJ), bad=rng.choice(BAD_ADJ),
        awful=rng.choice(AWFUL_ADJ), mid=rng.choice(MID_ADJ),
        boost=rng.choice(BOOST), days=rng.randint(2, 30), relative=rng.choice(RELATIVES))
    return text.replace("  ", " ")


def _sentences(rng, kind, product, aspects, count):
    pools = {"pos": POS_SENT, "neg": NEG_SENT, "mid": MID_SENT}
    out = []
    for _ in range(count):
        roll = rng.random()
        if kind == "pos" and roll < 0.12:
            pool = NEG_OF_BAD
        elif kind == "neg" and roll < 0.12:
            pool = NEG_OF_GOOD
        elif kind == "neg" and roll < 0.18:
            pool = SARCASM
        elif kind != "mid" and roll < 0.30:
            pool = MID_SENT
        else:
            pool = pools[kind]
        out.append(_fill(rng.choice(pool), rng, product, aspects))
    return out


def make_reviews(n, seed=7):
    """n product reviews; ratings 1-5 are skewed towards positive like real shops."""
    rng = random.Random(seed)
    products = list(PRODUCTS)
    rows = []
    for i in range(1, n + 1):
        product = rng.choice(products)
        aspects = PRODUCTS[product]
        rating = rng.choices([1, 2, 3, 4, 5], weights=[12, 9, 14, 27, 38])[0]
        kind = "neg" if rating <= 2 else "mid" if rating == 3 else "pos"
        count = rng.choices([1, 2, 3, 4, 5], weights=[15, 30, 30, 15, 10])[0]
        sents = _sentences(rng, kind, product, aspects, count)
        if kind == "mid" and rng.random() < 0.5:
            sents.append(_fill(rng.choice(POS_SENT if rng.random() < 0.5 else NEG_SENT),
                               rng, product, aspects))
        elif kind != "mid" and rng.random() < 0.2:
            other = "neg" if kind == "pos" else "pos"
            turn = _sentences(rng, other, product, aspects, 1)[0]
            sents.append("But " + turn[0].lower() + turn[1:])
        words = " ".join(sents).split(" ")
        words = [_typo(w, rng) if rng.random() < TYPO_RATE else w for w in words]
        text = " ".join(words)
        if rng.random() < 0.15:
            text = text.lower()
        if rng.random() < 0.05:
            text = text.upper()
        if rng.random() < 0.10:
            text = text.rstrip(".") + "!!"
        label = "negative" if rating <= 2 else "neutral" if rating == 3 else "positive"
        rows.append({"id": i, "product": product, "text": text, "rating": rating, "label": label})
    return rows


# ---------------------------------------------------------------- tickets

TICKETS = {
    "billing": [
        "I was charged twice for order {order}.",
        "My invoice for {month} shows the wrong amount of {amount}.",
        "Why did my card get charged {amount} this month?",
        "Please update the billing address on my account.",
        "The payment failed but the money left my account.",
        "Can I get a copy of the invoice for order {order}?",
        "I see an extra charge of {amount} that I do not recognise.",
    ],
    "shipping": [
        "Where is my order {order}? It has not arrived yet.",
        "The tracking number for {order} does not work.",
        "My package was delivered to the wrong address.",
        "Order {order} says delivered but I never got it.",
        "How long does shipping to {city} take?",
        "The parcel arrived damaged and the box was open.",
        "Can I change the delivery address for order {order}?",
    ],
    "account": [
        "I cannot log in to my account since {weekday}.",
        "Please reset the password for {email}.",
        "How do I change the email address on my account?",
        "My account was locked after too many login attempts.",
        "I want to delete my account and all my data.",
        "I never received the verification email at {email}.",
        "Someone else may have access to my account.",
    ],
    "technical": [
        "The app crashes every time I open the order page.",
        "I get error {error} when I try to pay.",
        "The website is very slow on my phone.",
        "The login page shows a blank screen.",
        "The app does not load my order history.",
        "Push notifications stopped working after the update.",
        "I get error {error} when I log in on the app.",
    ],
    "refund": [
        "I returned order {order} on {date} and still have no refund.",
        "When will I get my money back for {order}?",
        "I want a refund for the damaged item in order {order}.",
        "The refund of {amount} has not reached my card.",
        "Can I get a refund instead of a replacement?",
        "You refunded {amount} but I paid more than that.",
        "How long do refunds take to show on my card?",
    ],
}
OPENERS = ["Hi,", "Hello,", "Good morning,", "Hey there,", "", "", "Dear support,"]
CLOSERS = ["Thanks.", "Thank you!", "Please help.", "This is urgent!", "Regards, {name}", "",
           "", "Waiting for your answer."]
EXTRA = ["I have been a customer for {years} years.", "I already tried twice.",
         "This is the second time this happens.", "My order number is {order}.",
         "I paid with my credit card.", "I used the mobile app."]
NAMES = ["Ana", "Ben", "Chen", "Deniz", "Eva", "Femi", "Gus", "Hana", "Ivan", "Jo"]
CITIES = ["Berlin", "Lisbon", "Oslo", "Madrid", "Vienna", "Dublin", "Prague"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ERRORS = ["E401", "E403", "E500", "E502", "E1007"]
CATEGORY_WEIGHTS = {"shipping": 30, "technical": 25, "account": 20, "billing": 15, "refund": 10}


def _ticket_values(rng):
    return {
        "order": "ORD-%05d" % rng.randint(10000, 99999),
        "amount": "$%d.%02d" % (rng.randint(5, 300), rng.choice([0, 49, 90, 99])),
        "month": rng.choice(MONTHS),
        "city": rng.choice(CITIES),
        "weekday": rng.choice(WEEKDAYS),
        "email": "%s%d@example.com" % (rng.choice(NAMES).lower(), rng.randint(1, 99)),
        "error": rng.choice(ERRORS),
        "date": "2026-%02d-%02d" % (rng.randint(1, 9), rng.randint(1, 28)),
        "name": rng.choice(NAMES),
        "years": rng.randint(1, 9),
    }


def make_tickets(n, seed=11):
    """n support tickets; categories are imbalanced and share words on purpose."""
    rng = random.Random(seed)
    cats = list(CATEGORY_WEIGHTS)
    weights = [CATEGORY_WEIGHTS[c] for c in cats]
    rows = []
    for i in range(1, n + 1):
        cat = rng.choices(cats, weights=weights)[0]
        v = _ticket_values(rng)
        parts = [rng.choice(OPENERS)]
        main = rng.sample(TICKETS[cat], k=rng.choice([1, 1, 2]))
        parts += [t.format(**v) for t in main]
        if rng.random() < 0.15:
            other = rng.choice([c for c in cats if c != cat])
            parts.append(rng.choice(TICKETS[other]).format(**v))
        if rng.random() < 0.4:
            parts.append(rng.choice(EXTRA).format(**v))
        parts.append(rng.choice(CLOSERS).format(**v))
        text = " ".join(p for p in parts if p)
        words = [_typo(w, rng) if rng.random() < TYPO_RATE else w for w in text.split(" ")]
        text = " ".join(words)
        urgent = "urgent" in text.lower() or rng.random() < 0.1
        rows.append({"id": i, "text": text, "category": cat,
                     "priority": "high" if urgent else "normal"})
    return rows


# ---------------------------------------------------------------- messy text

# Characters that look like ordinary ones but are not (written with chr so the
# file itself stays plain ASCII).
NBSP = chr(0xA0)            # no-break space
ZWSP = chr(0x200B)          # zero-width space
RSQUO = chr(0x2019)         # right single quotation mark
LDQUO, RDQUO = chr(0x201C), chr(0x201D)
FW_EXCL = chr(0xFF01)       # full-width exclamation mark
ELLIPSIS = chr(0x2026)


def _mess(text, rng):
    words = text.split(" ")
    out = []
    for w in words:
        roll = rng.random()
        if roll < 0.06:
            out.append(w + NBSP)
        elif roll < 0.09:
            out.append(w + ZWSP + " ")
        elif roll < 0.13:
            out.append(w + "  ")
        else:
            out.append(w + " ")
    text = "".join(out).strip()
    text = text.replace("'", RSQUO) if rng.random() < 0.7 else text
    if rng.random() < 0.25:
        text = text.replace(" and ", " &amp; ")
    if rng.random() < 0.2:
        text = text.replace(". ", ".<br>", 1)
    if rng.random() < 0.15:
        text = "<p>" + text + "</p>"
    if rng.random() < 0.15:
        text = LDQUO + text + RDQUO
    if rng.random() < 0.1:
        text = text.rstrip(".!") + FW_EXCL
    if rng.random() < 0.1:
        text = text.rstrip(".!") + ELLIPSIS
    if rng.random() < 0.1:
        text = "\t" + text + "\n"
    return text


def messy_reviews(n, seed=5):
    """The first n reviews of make_reviews(n), copied from a web page: hidden
    spaces, curly quotes, HTML leftovers, full-width punctuation."""
    rng = random.Random(seed)
    rows = make_reviews(n)
    for row in rows:
        row["text"] = _mess(row["text"], rng)
    return rows


# ---------------------------------------------------------------- csv helpers

def _write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_reviews_csv(path, n, seed=7):
    _write(path, make_reviews(n, seed))


def write_tickets_csv(path, n, seed=11):
    _write(path, make_tickets(n, seed))
