"""Sample corpora for the Embeddings and Language Models lessons.

Every call with the same arguments returns exactly the same text on every
machine: the generators use their own random.Random(seed) and never the
global random module.

    make_corpus(n, seed=3)   -> list of n lowercase sentences (str) from a
                                small world: animals, food, vehicles, cities
                                and countries, people (male/female,
                                royal/young/family)
    WORD_CLASSES             -> the word lists behind the corpus
    CAPITALS                 -> city -> country pairs
    GENDER_PAIRS             -> (male, female) word pairs
    make_tagged(n, seed=13)  -> list of n sentences, each a list of
                                (word, tag) pairs; some words have two tags
                                ("book", "watch", "run", "light", ...)
    make_jobs(n, seed=21, skew=None) -> list of n sentences about occupations;
                                the pronoun is skewed by occupation (JOB_SKEW),
                                like the biased text embeddings learn from

Words in the same class are used in the same kinds of sentences, so their
meaning can be learned from the words around them.
"""
import random

ANIMALS = ["cat", "dog", "horse", "rabbit", "cow", "sheep", "goat", "mouse"]
FOODS = ["bread", "cheese", "apple", "rice", "soup", "cake", "pasta", "salad"]
VEHICLES = ["car", "bus", "bike", "train", "truck", "boat", "taxi", "tram"]
CAPITALS = {"paris": "france", "berlin": "germany", "rome": "italy", "madrid": "spain",
            "vienna": "austria", "lisbon": "portugal", "athens": "greece", "dublin": "ireland"}
COLORS = ["red", "blue", "green", "yellow", "black", "white"]
GENDER_PAIRS = [("man", "woman"), ("king", "queen"), ("boy", "girl"), ("prince", "princess"),
                ("father", "mother"), ("brother", "sister"), ("uncle", "aunt"), ("son", "daughter")]
ROYAL = {"king", "queen", "prince", "princess"}
YOUNG = {"boy", "girl", "prince", "princess", "son", "daughter"}

WORD_CLASSES = {
    "animal": ANIMALS,
    "food": FOODS,
    "vehicle": VEHICLES,
    "city": list(CAPITALS),
    "country": list(CAPITALS.values()),
    "color": COLORS,
    "person": [w for pair in GENDER_PAIRS for w in pair],
}

ANIMAL_VERBS = ["runs", "sleeps", "jumps", "rests", "hides"]
PLACES = ["field", "barn", "garden", "yard", "meadow"]
FOOD_ADJS = ["fresh", "warm", "sweet", "tasty", "cold"]
MEALS = ["breakfast", "lunch", "dinner"]
VEHICLE_ADJS = ["fast", "slow", "new", "old", "noisy"]
STOPS = ["station", "bridge", "corner", "garage", "depot"]


def _person_sentence(rng, word):
    male = any(word == m for m, _ in GENDER_PAIRS)
    pron, pos = ("he", "his") if male else ("she", "her")
    options = [
        f"{pron} is a {word}",
        f"the {word} smiled and {pron} waved",
        f"the {word} lost {pos} keys",
        f"the {word} took {pos} coat",
    ]
    if word in ROYAL:
        options += [f"the {word} sat on the throne", f"the {word} wore {pos} crown",
                    f"the {word} lives in the palace", f"the {word} rules the kingdom"]
    else:
        options += [f"the {word} lives in a small house", f"the {word} works in the town"]
    if word in YOUNG:
        options += [f"the young {word} went to school", f"the {word} played with {pos} toys"]
    else:
        options += [f"the {word} read the newspaper", f"the old {word} drank tea"]
    return rng.choice(options)


def _sentence(rng):
    kind = rng.choices(["animal", "food", "vehicle", "city", "person", "color"],
                       weights=[18, 18, 18, 14, 26, 6])[0]
    if kind == "animal":
        a, b = rng.sample(ANIMALS, 2)
        return rng.choice([
            f"the {a} {rng.choice(ANIMAL_VERBS)} in the {rng.choice(PLACES)}",
            f"the {a} chased the {b}",
            f"a small {a} drinks water",
            f"the farmer feeds the {a}",
            f"the {a} and the {b} sleep in the {rng.choice(PLACES)}",
        ])
    if kind == "food":
        f, g = rng.sample(FOODS, 2)
        return rng.choice([
            f"we ate {f} for {rng.choice(MEALS)}",
            f"the {f} is {rng.choice(FOOD_ADJS)}",
            f"she cooked {f} and {g}",
            f"i bought {f} at the market",
            f"the {f} tastes {rng.choice(FOOD_ADJS)}",
        ])
    if kind == "vehicle":
        v, w = rng.sample(VEHICLES, 2)
        city = rng.choice(list(CAPITALS))
        return rng.choice([
            f"the {v} stopped at the {rng.choice(STOPS)}",
            f"we took the {v} to {city}",
            f"the {v} is {rng.choice(VEHICLE_ADJS)}",
            f"the driver parked the {v}",
            f"the {v} passed the {w}",
        ])
    if kind == "city":
        city = rng.choice(list(CAPITALS))
        country = CAPITALS[city]
        return rng.choice([
            f"{city} is the capital of {country}",
            f"{city} is a big city in {country}",
            f"we flew to {city} in {country}",
            f"the people of {city} love {country}",
            f"{country} has a famous capital called {city}",
        ])
    if kind == "color":
        c = rng.choice(COLORS)
        thing = rng.choice(["door", "wall", "shirt", "flower", "bag"])
        return rng.choice([f"the {thing} is {c}", f"she painted the {thing} {c}",
                           f"a {c} {thing} was on the table"])
    return _person_sentence(rng, rng.choice(WORD_CLASSES["person"]))


def make_corpus(n, seed=3):
    """n lowercase sentences without punctuation; words are separated by spaces."""
    rng = random.Random(seed)
    return [_sentence(rng) for _ in range(n)]


# ---------------------------------------------------------------- tagged

# Tags: DET, NOUN, VERB, ADJ, ADP (preposition), PRON, ADV.
T_NOUNS = ["book", "watch", "light", "train", "park", "dog", "table", "letter", "game", "run"]
T_VERBS = ["book", "watch", "light", "train", "park", "read", "open", "play", "run", "like"]
T_ADJS = ["light", "old", "new", "red", "long", "quiet"]
T_PRONS = ["i", "you", "we", "they"]
T_ADPS = ["in", "on", "near", "after"]
T_ADVS = ["often", "today", "quickly", "again"]


def _tagged(rng):
    det = rng.choice(["the", "a"])
    noun, noun2 = rng.choice(T_NOUNS), rng.choice(T_NOUNS)
    adj = rng.choice(T_ADJS)
    template = rng.choice(["svo", "svo_adv", "det_adj_noun", "pron_verb_pp", "noun_verb"])
    if template == "svo":
        return [(rng.choice(T_PRONS), "PRON"), (rng.choice(T_VERBS), "VERB"),
                (det, "DET"), (noun, "NOUN")]
    if template == "svo_adv":
        return [(rng.choice(T_PRONS), "PRON"), (rng.choice(T_ADVS), "ADV"),
                (rng.choice(T_VERBS), "VERB"), (det, "DET"), (adj, "ADJ"), (noun, "NOUN")]
    if template == "det_adj_noun":
        return [(det, "DET"), (adj, "ADJ"), (noun, "NOUN"), (rng.choice(["is", "was"]), "VERB"),
                (rng.choice(T_ADPS), "ADP"), ("the", "DET"), (noun2, "NOUN")]
    if template == "pron_verb_pp":
        return [(rng.choice(T_PRONS), "PRON"), (rng.choice(T_VERBS), "VERB"),
                (rng.choice(T_ADPS), "ADP"), ("the", "DET"), (noun, "NOUN")]
    return [("the", "DET"), (noun, "NOUN"), (rng.choice(["was", "is"]), "VERB"),
            (rng.choice(["long", "quiet", "new", "old"]), "ADJ")]


def make_tagged(n, seed=13):
    """n sentences, each a list of (word, tag) pairs."""
    rng = random.Random(seed)
    return [_tagged(rng) for _ in range(n)]


# ---------------------------------------------------------------- occupations

# Share of "she" for each occupation: a deliberately biased text.
JOB_SKEW = {"nurse": 0.85, "secretary": 0.85, "dancer": 0.8, "florist": 0.8,
            "engineer": 0.15, "pilot": 0.15, "mechanic": 0.2, "plumber": 0.2,
            "teacher": 0.5, "writer": 0.5}


def make_jobs(n, seed=21, skew=None):
    """n sentences about occupations with gendered pronouns; `skew` maps each
    occupation to its share of "she" (default JOB_SKEW)."""
    skew = skew or JOB_SKEW
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        job = rng.choice(list(skew))
        pron, pos = ("she", "her") if rng.random() < skew[job] else ("he", "his")
        out.append(rng.choice([
            f"the {job} said that {pron} was tired",
            f"the {job} finished {pos} work",
            f"{pron} works as a {job}",
            f"the {job} took {pos} bag",
            f"the {job} went home after {pos} shift",
        ]))
    return out
