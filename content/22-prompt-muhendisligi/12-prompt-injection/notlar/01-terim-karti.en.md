| Term | Meaning |
|---|---|
| **Prompt injection** | An attack that changes the model's behaviour with an instruction in the data |
| **Direct attack** | The user writes the instruction themselves |
| **Indirect attack** | The instruction comes inside data such as a document, a web page or a tool result |
| **Input detector** | A layer that looks for attack patterns in the incoming text |
| **Canary** | A word put into the system message that appears nowhere else; if it shows in the answer, there is a leak |
| **Exfiltration** | Data being sent to another server through a link or an image address |
| **Least privilege** | The assistant having only the tools its job needs |

**Keep in mind:**

- In the lesson the detector's precision was 0.8 and its recall 0.57:
  "1gnore", the attack in another language and the "I am the admin"
  claim got through; an innocent message raised a false alarm.
- The output check caught the system message leak and links to two
  domains not on the allow-list; one was an image link.
- There is no known complete fix for this attack; the defence is layered
  and measured.
