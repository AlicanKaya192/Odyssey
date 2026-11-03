# SSRF: Server-Side Request Forgery

In CSRF the attacker made **the user's browser** send a request. In SSRF
(server-side request forgery) they get **the server** to do the same. Many
applications have features such as "fetch the image at this address",
"show a preview of the link" or "send a notification to this address": the
user gives an address and the server sends a request to it **on its own
behalf**. Because the server sits inside the internal network, it can
reach addresses that cannot be reached from outside. This section shows the
hole with a toy "internet" dictionary and builds its defences: an allow
list, checking the address by parsing it, rejecting internal addresses and
limiting at the network layer. No real request is sent; "fetching" is a
dictionary lookup.

## The hole: the server goes to any address

```python
FAKE_WEB = {
    "https://images.example.com/cat.png": "<cat image bytes>",
    "http://127.0.0.1/admin": "internal admin panel",
    "http://10.20.0.15/config": "internal settings page",
}


def fetch(url):
    return FAKE_WEB.get(url, "404")


def preview_bad(url):
    return fetch(url)


print(preview_bad("https://images.example.com/cat.png"))
print(preview_bad("http://127.0.0.1/admin"))
print(preview_bad("http://10.20.0.15/config"))
```

```text
<cat image bytes>
internal admin panel
internal settings page
```

The preview feature was written for images, but the user had it request
the server **itself** (`127.0.0.1`) and a server on the internal network
(`10.20.0.15`). These addresses cannot be reached from the internet; the
firewall had closed them to the outside (the Firewalls section). But
because the request came not from outside but **from the trusted server
inside**, the firewall did not step in. The weakness of the perimeter model
from the VPNs and Network Segmentation section shows up again here: if
being inside counts as a reason for trust, every feature that can send
requests inwards turns into a door.

On servers running in the cloud the risk is even greater: cloud
environments offer a **metadata service** that hands out the server's own
credentials at an address in the link-local range (`169.254.0.0/16`). An
attacker who reaches that address through SSRF can take over the server's
cloud permissions.

## The first defence: an allow list and a parser

If the feature is only meant to fetch images from certain sites, the most
solid defence is an **allow list**: the address is parsed and its scheme
and host are compared **exactly** with the list. As we saw in the HTTP and
HTTPS section, this comparison is not done with a text search:

```python
from urllib.parse import urlsplit

ALLOWED_HOSTS = {"images.example.com"}


def text_check(url):
    return url.startswith("https://images.example.com")


def allowed(url):
    parts = urlsplit(url)
    return parts.scheme in ("http", "https") and parts.hostname in ALLOWED_HOSTS


for url in ["https://images.example.com/cat.png",
            "http://127.0.0.1/admin",
            "https://images.example.com@127.0.0.1/admin",
            "file:///app/settings.ini"]:
    print(f"{text_check(url)!s:<5} {allowed(url)!s:<5} {url}")
```

```text
True  True  https://images.example.com/cat.png
False False http://127.0.0.1/admin
True  False https://images.example.com@127.0.0.1/admin
False False file:///app/settings.ini
```

The text check let the third address through: to the eye it looks like
`images.example.com`, but its real host is `127.0.0.1` (the part left of
the `@` is a user name). The check made with a parser refused it. The
`file://` scheme on the fourth line was refused too: schemes that read
files on the server's own disk are never accepted in a fetch feature.
**Only `http` and `https`.**

## The second defence: rejecting internal addresses

Sometimes an allow list cannot be built (the user wants a preview of any
site). Then we go the other way: addresses that **lead into the internal
network** are refused. The `ipaddress` module from the Network Layers
section knows which addresses are internal:

```python
import ipaddress


def is_internal(ip):
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_unspecified or ip.is_reserved)


for text in ["100.20.30.40", "127.0.0.1", "10.20.0.15",
             "169.254.169.254", "0.0.0.0"]:
    print(f"{text:<16} {is_internal(ipaddress.ip_address(text))}")
```

```text
100.20.30.40     False
127.0.0.1        True
10.20.0.15       True
169.254.169.254  True
0.0.0.0          True
```

Loopback, the private ranges, the metadata address in the link-local range
and `0.0.0.0`, which means "no address", were counted as internal; only the
public address passed.

But addresses often come **by name**. Looking at the name itself is not
enough: a name that sounds like a site outside can resolve to an internal
address in DNS. The check is made **after resolution**, on the IP address
the name really goes to (we imitate DNS with a dictionary again):

```python
from urllib.parse import urlsplit

DNS = {"images.example.com": "100.20.30.40",
       "intranet.example.net": "10.20.0.15"}


def safe_target(url):
    host = urlsplit(url).hostname
    try:
        ip = ipaddress.ip_address(DNS.get(host, host))
    except ValueError:
        return "unknown host"
    return "blocked" if is_internal(ip) else f"ok {ip}"


for url in ["https://images.example.com/a.png",
            "https://intranet.example.net/",
            "http://127.0.0.1/admin",
            "https://nowhere.example/"]:
    print(safe_target(url))
```

```text
ok 100.20.30.40
blocked
blocked
unknown host
```

The name `intranet.example.net` looks harmless, but it was refused because
it resolves to `10.20.0.15`. The name that could not be resolved was
refused too: staying closed when unsure (fail securely from the Security
Principles section).

Two more details:

- **Connect to the address you checked.** If the name is resolved again
  after the check, it may have turned into a different address in the
  meantime (if the DNS record's TTL is very short). The right way is to
  resolve the name once, check it, and open the connection **to the checked
  IP address**.
- **Watch out for redirects.** An allowed server can redirect with a `301`
  to an internal address. The fetch feature either never follows redirects
  or repeats the same check at every step.

## The third defence: limiting at the network layer

If something slips through in the code, the network is the last layer:

- The component that does the fetching runs in a separate zone and, with
  **egress filtering** (the Firewalls section), can only go out to the
  internet; it has no path to the internal network or the metadata
  address.
- Internal services do not skip authentication because "the request comes
  from inside" (zero trust from the VPNs and Network Segmentation
  section).
- The protected version of the cloud metadata service, which requires a
  special header or token on each request, is switched on.

## Limit the response too

Showing the fetched content to the user as it is carries internal systems'
responses outside. The preview feature accepts only the type it expects
(for example an image) and only up to a certain size; on an error the user
gets a general message, not internal details. The timeout is kept short: an
address that does not answer must not use up the server's resources.

<figure class="fig anat">
  <div class="anat-row"><span>Allow list</span><span>Scheme and host exactly matching the list; the most solid.</span></div>
  <div class="anat-row"><span>Parser</span><span><code>urlsplit(url).hostname</code>; not a text search.</span></div>
  <div class="anat-row"><span>Rejecting internal addresses</span><span>On the IP after resolution; private, loopback, link-local, reserved.</span></div>
  <div class="anat-row"><span>Connection and redirects</span><span>Connect to the checked IP; do not follow redirects or re-check every step.</span></div>
  <div class="anat-row"><span>Network</span><span>Egress filtering for the fetch component; authentication in internal services.</span></div>
  <figcaption>Layers against SSRF. If one slips, the others hold.</figcaption>
</figure>

## Summary

- **SSRF:** the server sends a request on its own behalf to an address the
  user gives; because it sits inside, it reaches addresses that cannot be
  reached from outside.
- In the cloud, the **metadata service** in the link-local range is a
  special risk.
- The most solid defence is an **allow list**: the address is **parsed**,
  and the scheme (`http`, `https`) and host are compared exactly.
- If an allow list cannot be built, **internal addresses are refused**; the
  check is made **on the IP** after the name is resolved, and the
  connection is opened to the checked IP.
- Redirects are not followed, or are re-checked at every step.
- At the network layer, **egress filtering** for the fetch component;
  internal services do not skip authentication.
- The response type, size and timeout are limited; error details are not
  shown.
