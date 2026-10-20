| Term | Meaning |
|---|---|
| **MLOps** (machine learning operations) | Applying the ideas of DevOps to machine learning systems: code, data and model are tested, versioned and watched together. |
| **Churn** | A customer cancelling their subscription; what this module predicts. |
| **Notebook** | A working page that holds code, output and notes together; good for experimenting, not enough for a system. |
| **Life cycle** | Data → train → evaluate → serve → monitor, then data again. |
| **Serving** | Making the model usable by whoever needs predictions, for example by putting it behind an API. |
| **Monitoring** | Regularly watching the incoming data and the success of the model in production. |
| **Silent failure** | The model getting worse without raising an error, while it keeps producing predictions. |
| **Retraining** | Training the model again from scratch on new data. |
| **Continuous training** | The model being retrained and evaluated automatically when new data arrives. |
| **Technical debt** | The later cost of a shortcut taken today; in ML it builds up in the data and the process. |
| **Seed** | The starting value of a random number generator; the same seed gives the same numbers every time. |
| **Maturity level** | Level 0 manual, level 1 an automated training pipeline, level 2 the pipeline itself in CI/CD. |

An ML system has **three things** that can change, and all three are watched together:

- **Code:** the training and feature preparation code
- **Data:** the data that goes into training
- **Model:** the file that training produces
