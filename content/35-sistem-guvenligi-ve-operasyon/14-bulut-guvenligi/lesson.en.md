# Cloud Security

Today many systems run not on servers in the organisation's own room but
in the data centres of a **cloud provider**. Renting a server, storage or a
ready-made application is fast and reduces the maintenance load. But the
security responsibility does not disappear; it is **shared**. Most
incidents in the cloud come not from a flaw at the provider but from a
**configuration mistake** by the customer: a storage area left public, a
privilege wider than needed, a management port opened to the internet.

This section covers shared responsibility and small tools that check for
the most common configuration mistakes. All configurations are fake dicts;
no cloud service is contacted.

## Shared responsibility

Cloud services fall into three models depending on how much the provider
takes on:

| Model | What is rented | Example |
|---|---|---|
| **IaaS** (infrastructure) | Virtual servers, network, storage | A virtual machine where you install your own operating system |
| **PaaS** (platform) | The environment the application runs in | An application platform you upload your code to |
| **SaaS** (software) | A ready-made application | An email or document service |

The more the provider takes on, the less is left to the customer, but
**data and identities** belong to the customer in every model:

```python
LAYERS = ["data", "identities", "application", "operating system", "network", "physical"]
for model, provider_from in [("IaaS", 4), ("PaaS", 3), ("SaaS", 2)]:
    print(f"{model}: you = {', '.join(LAYERS[:provider_from])}")
```

```text
IaaS: you = data, identities, application, operating system
PaaS: you = data, identities, application
SaaS: you = data, identities
```

Even with SaaS, who can reach which document, which account uses
multi-factor authentication and which data is put there are the
customer's responsibility. "It is in the cloud, the provider protects it"
is the most common misconception.

## Storage areas

In the cloud, files are usually kept in **object storage** areas
(buckets). An area left **public** by mistake is the best-known cause of
data leaks in the cloud. The check looks at who each area is open to, what
kind of data it holds and whether it is encrypted:

```python
BUCKETS = [
    {"name": "web-assets", "public": True, "encrypted": True, "data": "public"},
    {"name": "customer-exports", "public": True, "encrypted": False, "data": "personal"},
    {"name": "logs", "public": False, "encrypted": True, "data": "internal"},
]
for b in BUCKETS:
    problems = []
    if b["public"] and b["data"] != "public":
        problems.append("public but holds " + b["data"] + " data")
    if not b["encrypted"]:
        problems.append("not encrypted")
    print(f"{b['name']}: {'; '.join(problems) or 'ok'}")
```

```text
web-assets: ok
customer-exports: public but holds personal data; not encrypted
logs: ok
```

The website's images being public is natural. Customer exports sitting
public and unencrypted is an incident. Most providers offer an
account-level setting such as "block public access"; the secure default
(the Secure Software Development section) is having it switched on.

## Identity and access policies

What can be done in the cloud is decided by **identity and access
management** (IAM) policies. A policy is made of statements that allow
(`allow`) and forbid (`deny`); action names can use the `*` wildcard. The
common rules: everything not explicitly allowed is forbidden, and **deny
always wins**:

```python
from fnmatch import fnmatchcase

POLICY = [
    {"effect": "allow", "action": "storage:Get*"},
    {"effect": "allow", "action": "storage:List*"},
    {"effect": "deny", "action": "storage:GetSecret*"},
]


def allowed(policy, action):
    matches = [s["effect"] for s in policy if fnmatchcase(action, s["action"])]
    if "deny" in matches:
        return False
    return "allow" in matches


for action in ["storage:GetObject", "storage:GetSecretValue", "storage:DeleteObject"]:
    print(action, allowed(POLICY, action))
```

```text
storage:GetObject True
storage:GetSecretValue False
storage:DeleteObject False
```

Reading objects is allowed. Reading secrets also fits the `Get*` pattern,
but a separate deny statement closed it: deny won. There is no statement at
all for deleting; it was refused by default. The wildcard is convenient but
dangerous: a permission such as `storage:*`, or just `*`, is the exact
opposite of the principle in the Least Privilege and Separation of Duties
section and the first thing flagged in a review.

## Network rules

Traffic reaching cloud servers is limited by **security groups** or
similar network rules (the Firewalls section). The most common mistake is
opening management ports (remote access, databases) to the whole internet
(`0.0.0.0/0`):

```python
RULES = [
    {"port": 443, "source": "0.0.0.0/0"},
    {"port": 22, "source": "0.0.0.0/0"},
    {"port": 5432, "source": "10.0.0.0/16"},
    {"port": 3389, "source": "0.0.0.0/0"},
]
ADMIN_PORTS = {22, 3389, 5432}
for r in RULES:
    if r["port"] in ADMIN_PORTS and r["source"] == "0.0.0.0/0":
        print("open to the internet:", r["port"])
```

```text
open to the internet: 22
open to the internet: 3389
```

The web port `443` being public is the point. The remote access ports `22`
and `3389`, however, are open to the whole internet: they become targets
for password guessing from anywhere in the world. The database is
reachable only from the internal network; that is right. Management access
is limited through a VPN or a similar intermediate layer and to specific
addresses.

## Infrastructure as code

When cloud resources are set up not by clicking but with a configuration
file (**infrastructure as code**), all these checks can be done **before**
setup: the file is scanned as in the Code Review and Static Analysis
section, and findings such as a public bucket or `0.0.0.0/0` stop the
change. The wrong configuration never reaches the cloud.

## Summary

- Security in the cloud is **shared**: the provider protects the
  infrastructure, **data and identities** belong to the customer in every
  model.
- Most incidents come not from a provider flaw but from a **configuration
  mistake**.
- Storage areas are **closed** and encrypted by default.
- In IAM, what is not explicitly allowed is forbidden, **deny wins**; broad
  wildcard permissions are avoided.
- Management ports are not opened to the whole internet.
- **Infrastructure as code** moves the checks to before setup.
