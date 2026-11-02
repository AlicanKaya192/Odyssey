A piece of the risk register of a small school system. The scores and
levels were computed with Python (the level boundaries are the same as in
the lesson).

| Risk | Likelihood | Impact | Score | Level | Owner | Answer |
|---|---|---|---|---|---|---|
| A teacher account's password is guessed | 4 | 4 | 16 | High | Ayşe | Mitigate: second step (MFA) |
| The grades database leaks | 2 | 5 | 10 | High | Mehmet | Mitigate: encryption, access review |
| The site crashes on exam day | 3 | 3 | 9 | Medium | Can | Mitigate: a second server |
| Fire in the server room | 1 | 5 | 5 | Medium | Zeynep | Transfer: insurance; plus backups |
| A small flaw on an old test server | 2 | 2 | 4 | Low | Can | Accept: look again in 3 months |

## The columns

- **Risk:** a short, concrete name. Not "cyber attack", but "a teacher
  account's password is guessed".
- **Likelihood, impact, score:** the score is always the product; it is not
  typed by hand.
- **Owner:** the one person responsible for the risk. Not "IT", a name.
- **Answer:** mitigate, transfer, avoid or accept; with what will be done.

## How is it read?

1. Start from the highest score.
2. Does every critical and high risk have an answer and a date?
3. For the accepted ones, is it written who accepted them and when?
4. After a control is applied, likelihood or impact is scored again; the
   old score is not deleted, the new one is written next to it. That shows
   whether the control worked.

## When is it updated?

- At regular intervals (for example every three months).
- When a new system, a new kind of data or a new supplier arrives.
- After an incident: if the incident showed a risk that was not in the
  register, it is added.
