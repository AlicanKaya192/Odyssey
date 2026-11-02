The question of separation of duties is always the same: **if one person
can do all these steps, what harm can they do?** Examples of conflicting
duties from different areas:

| Area | First duty | Conflicting duty | If one person holds both |
|---|---|---|---|
| Purchasing | Registering a supplier | Approving the payment | Sending money to a fake company |
| Payroll | Adding an employee | Starting the salary payment | Salary for a "ghost" employee who does not exist |
| Software | Writing code | Sending code to production alone | Unreviewed code with a back door |
| Access | Requesting a privilege | Approving your own privilege | Unlimited privileges |
| Logging | Taking actions in the system | Deleting the log files | Wiping out the traces |
| Warehouse | Receiving goods | Approving the stock count | Hiding missing goods |

## What do small teams do?

In a team of five it can be hard to find a separate person for every step.
Then **compensating controls** are used:

- If there is no separate person, review afterwards: at the end of the
  month someone else goes through all the payments.
- Copying logs to a place where they cannot be changed: whoever takes an
  action cannot delete its record.
- Thresholds: small amounts with one approval, large ones with two.

## Traps of the two-person rule

- **Two accounts of the same person:** it must be checked that the
  approver really is someone else.
- **Glancing and approving:** if the second person does not understand what
  they are approving, the rule exists only on paper.
- **Approving your own request:** if the requester and the approver are the
  same, the system should refuse.
