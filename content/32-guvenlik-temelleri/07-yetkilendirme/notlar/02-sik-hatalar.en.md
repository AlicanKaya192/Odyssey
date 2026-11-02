Authorization mistakes are often a single line and go unnoticed in
testing: the person testing is already looking at their own data. The
common ones:

## Checking only in the interface

The admin menu is hidden from ordinary users, but the address the menu
calls is open to everyone. When the user sends the request by hand, the
action is carried out. **Fix:** put the check in the code that handles the
request; hiding in the interface is only a convenience.

## Trusting the client

A `role=admin` field sent with the request, a hidden form field or a role
value written in plain text in a cookie is used. The user can change all of
these. **Fix:** read the role from the user's record on the server.

## Not asking who owns the object (IDOR)

The address `/orders/5512` returns the order, but nobody asks whether the
order belongs to this user. **Fix:** add the owner to the query ("this
user's order 5512") and say "not found" if there is none.

Using unguessable identifiers (long random values) instead of sequence
numbers makes it harder, but it **does not replace** the check; once an
identifier is shared in a link, it opens again.

## Forgetting bulk actions

Deleting one record is checked, "delete selected" is not. Or the listing
page filters, but the export (download CSV) gives everything. **Fix:** call
the same decision function on every path.

## Default allow

A newly added endpoint has no check, because it "will be added later".
**Fix:** at the framework level, make the default "login and permission
required"; an endpoint meant to be public is marked explicitly.

## Giving information away in error messages

Saying "you are not authorised" for someone else's invoice and "not found"
for an invoice that does not exist tells which numbers exist. **Fix:** give
the same answer to both ("not found").
