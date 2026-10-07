Let's read the documentation of an imaginary school API through REST eyes.

## The documentation

```text
GET    /students                 all students
GET    /students/17              one student
POST   /students                 a new student
PATCH  /students/17              change a field of the student
DELETE /students/17              delete the student
GET    /students/17/grades       the student's grades
POST   /students/17/grades       add a grade to the student
GET    /courses?teacher=ada      Ada's courses
POST   /sendReportCard           send a report card
GET    /students/17/remove       remove the student
```

## Judging it

The first eight lines follow REST: plural collections, items by identifier, a
nested relationship (`/students/17/grades`), filtering in the query
(`?teacher=ada`).

The last two lines have problems:

- `POST /sendReportCard`: a verb in the address. In REST, an action has to be
  turned into a resource: "sending a report card" can be a resource:
  `POST /students/17/report-cards`.
- `GET /students/17/remove`: a `GET` that deletes something. If a browser
  preloaded this address or a search engine crawled it, the student would be
  deleted. The right one is already in the documentation:
  `DELETE /students/17`.

## Turning an action into a resource

Some jobs do not look like "nouns": sending an email, making a payment,
re-running a report. In REST they are usually thought of as **a record being
created**:

| Action | As a resource |
|---|---|
| Send a report card | `POST /report-cards` |
| Make a payment | `POST /payments` |
| Reset a password | `POST /password-resets` |
| Re-run a report | `POST /reports/7/runs` |

That way every job has a record, and its status can be checked with
`GET /payments/123`.
