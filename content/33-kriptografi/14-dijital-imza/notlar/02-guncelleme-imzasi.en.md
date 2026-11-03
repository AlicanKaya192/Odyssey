A software update is the most familiar use of a signature: with the
signature, the program learns that the file it downloaded really came from
the maker and was not changed on the way.

<figure class="fig">
<div class="flow">
<span class="node">The maker signs the package</span>
<span class="arrow">→</span>
<span class="node">Package + signature downloaded</span>
<span class="arrow">→</span>
<span class="node acc">Verify with the built-in public key</span>
<span class="arrow">→</span>
<span class="node acc">Is the version newer?</span>
<span class="arrow">→</span>
<span class="node ok">Install</span>
</div>
<figcaption>A safe update: if the signature does not match or the version goes backwards, nothing is installed.</figcaption>
</figure>

## Why the public key is inside the program

If the verification key were downloaded with the update, someone who
changed the package could change the key too. The key is built into the
program in advance, or comes from a certificate chain the operating system
trusts.

## Why the version is checked too

An old version was also **validly** signed by the maker. Offering an old
version with a known flaw as an "update" passes the signature check. That
is why the version number goes into the signed information and the program
does not install a version that **goes backwards**.

## What the signature does not protect

- Harmful code that got onto the maker's own build machine is signed too;
  the signature says "the maker signed it", not "the code is harmless".
- If the private key is stolen, an attacker can make valid signatures. That
  is why the signing key is kept in a separate, protected place (such as a
  hardware security module) and must be revocable if needed.
