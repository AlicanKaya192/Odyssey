**Your first MLOps pipeline in your own project**

1. Put training in a single script: the seed, the settings and the data's
   digest written to a record. Run it twice with the same settings and see
   the same result.
2. Write a schema for the data; check it before training.
3. Set up a baseline and a simple gate: a new model isn't registered
   unless it beats it.
4. Serve the model and log every prediction with its version.
5. Measure accuracy when the labels arrive; measure drift every day.
6. Tie the pipeline to a workflow: on a schedule and by hand.

After every step, break something on purpose to see the pipeline really
stop (shift a column, remove the seed): a gate that doesn't stop anything
isn't a gate.

**What we wrote ourselves in this module**

We built every piece with a few lines; in real projects ready-made tools
do the same jobs:

| What we wrote | Examples of ready-made tools |
|---|---|
| Content-addressed store and pointer file | DVC |
| Experiment record and model registry | MLflow |
| Schema checking | pandera |
| Feature store | Feast |
| Monitoring and alerts | Prometheus, Grafana |

The tools' versions and details change over time; when setting them up,
look at their own documentation. But what they look at are the things you
measured in this module.

**Where to from here in Odyssey?**

- **CI/CD and DevOps:** the workflows this module's pipelines rest on.
- **Docker:** putting the model in an image and running it in the same
  environment.
- **Writing REST APIs with FastAPI:** building the service that serves the
  model in depth.
- **Big Data:** when the training data doesn't fit on one computer.

**Practical tips**

1. Set up the capstone pipeline with your own small dataset.
2. Read the pipeline's line every month; write down the reason for the
   `kept out` and `data rejected` lines.
3. Write the design document before the code; take the thresholds from it.
4. Before setting a new threshold, measure the noise first.
