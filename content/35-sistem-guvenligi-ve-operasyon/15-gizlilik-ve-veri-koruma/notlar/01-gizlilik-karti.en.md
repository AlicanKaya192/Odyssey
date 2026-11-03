## Concepts

| Concept | Meaning |
|---|---|
| Personal data | Any information about an identifiable natural person |
| Special category data | Sensitive data such as health, biometric, genetic, religion, political opinion |
| Data subject | The person whose data is processed |
| Controller | Whoever decides the purpose and the means |
| Processor | Whoever processes on the controller's behalf |
| Pseudonym | A value that replaces a direct identifier; the data is still personal |
| Anonymous data | Data that identifies no one, with any additional information |
| Indirect identifier | Fields that point to a person when combined: age, postcode, gender |

## From principle to code

| Principle | In code |
|---|---|
| Data minimisation | A list of allowed fields per purpose |
| Storage limitation | A period per purpose; a regular job that deletes what has expired |
| Pseudonym | `hmac.new(key, value, sha256)`; the key in the secrets vault |
| Anonymity check | k-anonymity: the smallest group size |
| Right of access | A data inventory + searching by person |
| Right to erasure | Deleting in every table and in the backup plan |

## Python patterns

- Filtering fields: `{k: v for k, v in record.items() if k in allowed}`.
- A keyed hash: `hmac.new(key, value.encode(), hashlib.sha256).hexdigest()`.
- Generalising: `age // 10 * 10`, `postcode[:3] + "**"`.
- The k value: `min(Counter(groups).values())`.

## Keep in mind

- Data that is not collected cannot leak.
- A plain hash is not enough for a pseudonym; it is reversed by trying
  possible values.
- Deleting the name is not anonymising.
- Expired data is deleted; "it might be useful" is not a purpose.
- This card is not legal advice; for details, consult the law itself and an
  expert.
