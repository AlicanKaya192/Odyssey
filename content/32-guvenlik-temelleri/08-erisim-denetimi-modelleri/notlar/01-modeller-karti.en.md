| | **DAC** | **MAC** | **RBAC** | **ABAC** |
|---|---|---|---|---|
| Stands for | Discretionary | Mandatory | Role-based | Attribute-based |
| Who decides? | The object's owner | The system | The administrator who defines roles | Written rules |
| Based on? | The owner's wish | Classification label and clearance | The person's role | Subject, object, action, environment |
| Strong side | Flexible, easy | A person cannot bend the rule | Easy to manage | Very fine-grained rules |
| Weak side | Owners make mistakes, Trojan horses | Rigid, laborious | Role explosion | Complex, hard to review |
| Example | Sharing a file | Classified documents | Teacher/student in a school | "During working hours, in their own department" |

## Terms

- **Owner:** in DAC, the person who decides about the object.
- **Classification:** the object's label.
- **Clearance:** the person's label.
- **Trojan horse problem:** a program the user opens runs with all of the
  user's privileges.
- **Role hierarchy:** one role inheriting the permissions of another.
- **Role explosion:** roles opened for exceptions multiplying until they
  cannot be managed.
- **Attribute:** a property used in the decision rule (department, time,
  device...).

## Which one when?

- Personal files, small teams: **DAC**.
- Classified information, strict rules: **MAC**.
- In-house applications with clear job descriptions: **RBAC**.
- Context-dependent rules (time, location, relationship): **RBAC + ABAC**.
