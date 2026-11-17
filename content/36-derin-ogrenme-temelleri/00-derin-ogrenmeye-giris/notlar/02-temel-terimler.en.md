Words that come up often in this module. We look at each one in detail in
its own section; here the short definitions stand together.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Tensor</span><span>PyTorch's multi-dimensional array of numbers; like a NumPy array, and it can carry derivatives too.</span></div>
    <div class="anat-row"><span>Layer</span><span>A building block that turns an input into an output, such as <code>nn.Linear</code>.</span></div>
    <div class="anat-row"><span>Parameter</span><span>The numbers adjusted by training: weights and constants (biases).</span></div>
    <div class="anat-row"><span>Forward pass</span><span>Passing the input through the layers to compute the output.</span></div>
    <div class="anat-row"><span>Loss</span><span>A function that measures with one number how wrong the prediction is.</span></div>
    <div class="anat-row"><span>Gradient</span><span>The derivative of the loss with respect to each parameter: which way the loss goes when the parameter grows a little.</span></div>
    <div class="anat-row"><span>Backpropagation</span><span>Computing the gradients with the chain rule from the end back to the start; <code>backward()</code> in PyTorch.</span></div>
    <div class="anat-row"><span>Optimizer</span><span>The algorithm that updates the parameters from the gradients; <code>SGD</code>, <code>Adam</code>.</span></div>
    <div class="anat-row"><span>Learning rate</span><span>How far to move at each update.</span></div>
    <div class="anat-row"><span>Epoch</span><span>Using the whole training data once.</span></div>
    <div class="anat-row"><span>Batch</span><span>The examples used together in one update; a small one is a mini-batch.</span></div>
  </div>
  <figcaption>The module's basic words.</figcaption>
</figure>

The word "deep" comes from the number of layers: a network with several
layers between the input and the output is called a deep network. The
lesson's network has one hidden layer; as we add layers later, the same
four-step training will not change at all.
