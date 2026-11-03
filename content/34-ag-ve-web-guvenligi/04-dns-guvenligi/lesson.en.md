# DNS Security

When you type a domain name into the browser, your computer first has to
find that name's IP address; as we saw in the Network Layers section,
packets travel by address, not by name. **DNS** (the Domain Name System)
does this translation. DNS is the internet's phone book, and whoever can
change a line in the book can send people wherever they like. This section
explains how DNS works, where it is open to attack and how it is
protected. The example names are `example.com`, `example.net` and
`.example`, which are reserved for documentation; no query is actually
sent.

## How does DNS work?

A name is a **hierarchy** read from right to left: at the top the root,
then a top-level domain (TLD) such as `com`, then the `example.com` domain
itself. Each domain's records are held by that domain's **authoritative**
server. Your computer usually asks the **resolver** of its internet
provider or company; if needed, the resolver asks from the root down to the
authoritative server and brings the answer back.

<figure class="fig"><div class="flow">
  <span class="node">Computer</span><span class="arrow">→</span>
  <span class="node">Resolver</span><span class="arrow">→</span>
  <span class="node">Root, TLD</span><span class="arrow">→</span>
  <span class="node acc">Authoritative</span>
</div><figcaption>The resolver follows the chain, finds the answer and keeps it in its cache for a while.</figcaption></figure>

Common record types:

<figure class="fig anat">
  <div class="anat-row"><span><b>A</b> / <b>AAAA</b></span><span>The name's IPv4 / IPv6 address.</span></div>
  <div class="anat-row"><span><b>CNAME</b></span><span>"This name is really an alias of that name." Resolution continues with the target name.</span></div>
  <div class="anat-row"><span><b>MX</b></span><span>The server that accepts the domain's e-mail.</span></div>
  <div class="anat-row"><span><b>NS</b></span><span>The domain's authoritative servers.</span></div>
  <div class="anat-row"><span><b>TXT</b></span><span>Free text; information such as e-mail verification rules lives here.</span></div>
  <figcaption>The DNS records of a domain. Each one is a "for this name, this information" pairing.</figcaption>
</figure>

Let us imitate a resolver with a dictionary. On a CNAME it continues with
the target name; on an A record it stops:

```python
RECORDS = {
    "example.com": ("A", "203.0.113.10"),
    "www.example.com": ("CNAME", "example.com"),
    "shop.example.com": ("CNAME", "cdn.example.net"),
    "cdn.example.net": ("A", "198.51.100.20"),
}


def resolve(name):
    steps = [name]
    while True:
        record = RECORDS.get(name)
        if record is None:
            return steps, "NXDOMAIN"
        kind, value = record
        if kind == "A":
            return steps, value
        name = value
        steps.append(name)


for name in ["www.example.com", "shop.example.com", "mail.example.com"]:
    steps, answer = resolve(name)
    print(" -> ".join(steps), "=", answer)
```

```text
www.example.com -> example.com = 203.0.113.10
shop.example.com -> cdn.example.net = 198.51.100.20
mail.example.com = NXDOMAIN
```

`NXDOMAIN` means "no such name". `shop.example.com` points to another
domain (`example.net`): the shop's pages may sit on a content delivery
network. Such outside pointers will turn into a risk below.

## Cache and TTL

Starting from the root on every query would be far too slow. The resolver
keeps the answer in a **cache**; the record's **TTL** (time to live, in
seconds) says for how long:

```python
cache = {}


def lookup(name, now, ttl=300):
    entry = cache.get(name)
    if entry and now < entry[1]:
        return entry[0], "cache"
    answer = resolve(name)[1]
    cache[name] = (answer, now + ttl)
    return answer, "asked"


for now in [0, 100, 299, 300, 450]:
    print(now, *lookup("www.example.com", now))
```

```text
0 203.0.113.10 asked
100 203.0.113.10 cache
299 203.0.113.10 cache
300 203.0.113.10 asked
450 203.0.113.10 cache
```

The first query went down the authoritative chain; the later ones came
from the cache until second 300. The cache makes DNS fast, but it has a
security consequence too: **if a wrong answer gets into the cache, everyone
using that resolver gets the same wrong answer until the TTL runs out.**

## Cache poisoning

DNS queries mostly travel over UDP (the Network Layers section): there is
no connection; the resolver sends the question and accepts the first
answer that looks right. If an attacker manages to deliver a fake answer
**before** the real one, the resolver writes it into the cache. This is
called **cache poisoning**; after that, everyone asking for `bank.example`
goes to the attacker's address.

The resolver checks two things to decide "is this answer to my question?":
the question's 16-bit **query ID** and the **source port** the question was
sent from. Old resolvers always used the same port; the only thing the
attacker had to guess was the query ID:

```python
ids = 2 ** 16
ports = 65535 - 1024 + 1
print(ids)
print(ids * ports)
```

```text
65536
4227858432
```

When only the query ID is random there are 65536 possibilities, a number a
fast attacker can hit in a short time. When the source port is also chosen
at random between 1024 and 65535, the possibilities pass four billion.
Today's resolvers randomise both. This makes guessing harder but does not
**verify** the answer; the real solution is to sign the answers.

## DNSSEC: signed answers

**DNSSEC** signs DNS records with digital signatures (the Digital
Signatures section of the Cryptography module). The resolver verifies the
signature with the domain's public key; a fake answer's signature does not
match. But how do we know the domain's public key is genuine? The parent
domain (`com`) publishes a **hash** of the child domain's key in its own
signed record (the DS record). This builds a **chain of trust** from the
root down. One link of the chain is a hash comparison:

```python
import hashlib
import hmac

child_key = "example.com zone key 2026"
published = hashlib.sha256(child_key.encode()).hexdigest()


def key_ok(presented):
    digest = hashlib.sha256(presented.encode()).hexdigest()
    return hmac.compare_digest(digest, published)


print(key_ok(child_key))
print(key_ok("example.com forged key"))
```

```text
True
False
```

A key that does not match the hash published by the parent was refused. In
real DNSSEC the keys are public keys and the signatures are digital
signatures; this is only a toy that shows the chain's idea, "the one above
knows the one below by its hash". DNSSEC provides integrity and
authenticity, **not confidentiality**: the queries can still be read.

## Privacy: encrypted DNS

Plain DNS queries are unencrypted. Someone listening to the network can
see which sites you visit from the names you ask for, even if the pages
themselves are encrypted with HTTPS. **Encrypted DNS** carries the queries
inside TLS: **DoT** (DNS over TLS) on a separate port, **DoH** (DNS over
HTTPS) inside ordinary HTTPS traffic. This stops eavesdropping and changes
on the way; but the resolver itself still sees the queries, so you are
choosing whom to trust.

## Other DNS risks

- **Hijacking the settings:** if an attacker changes the DNS setting of a
  home router or a computer to their own resolver, every query goes to
  them. The router's default management password is changed and its
  software kept up to date.
- **Takeover of the domain account:** someone who gets into the account
  where you registered the domain can change the NS records and take the
  whole domain. MFA is a must on this account.
- **Dangling CNAME:** if `shop.example.com` keeps pointing at an outside
  service that is no longer used, whoever registers that name on the
  service first can publish whatever they want on `shop.example.com`. This
  is called **subdomain takeover**. Defence: when you shut down a service,
  also delete the DNS record pointing at it, and review the records
  regularly.
- **Lookalike names** (typosquatting): registering a name with one letter
  changed from `example.com` and using it for phishing.

One way to catch lookalike names is **edit distance**: how many letters
must be added, removed or changed to turn one name into the other?

```python
def distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


for name in ["example.com", "examp1e.com", "exmaple.com", "example.co", "sample.org"]:
    d = distance(name, "example.com")
    flag = "LOOKALIKE" if 0 < d <= 2 else ""
    print(f"{name:<12} {d:>2}  {flag}".rstrip())
```

```text
example.com   0
examp1e.com   1  LOOKALIKE
exmaple.com   2  LOOKALIKE
example.co    1  LOOKALIKE
sample.org    5
```

The names with `1` written for `l` and with two letters swapped were
flagged because their distance is 1–2. Organisations watch new
registrations that look like their own name this way; on the user's side
the defence is using a bookmark instead of typing the address, and
reading the address bar.

## Summary

- **DNS** turns names into addresses; a name is a hierarchy (root, TLD,
  domain), and the resolver follows the chain.
- Record types: **A/AAAA** address, **CNAME** alias, **MX** e-mail, **NS**
  authoritative server, **TXT** text.
- Answers stay in the cache for the **TTL**; so do wrong answers.
- **Cache poisoning** puts a fake answer into the cache; a random query ID
  and source port make guessing harder.
- **DNSSEC** signs records; the parent publishes the hash of the child's
  key (chain of trust). It does not provide confidentiality.
- **Encrypted DNS** (DoT, DoH) protects queries from eavesdropping and
  changes; the resolver still sees them.
- Dangling CNAMEs, hijacked settings and lookalike names are DNS risks too;
  records are reviewed regularly.
