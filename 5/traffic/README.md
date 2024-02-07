# Traffic Lab Report

Dataset: [GTSRB](https://cdn.cs50.net/ai/2023/x/projects/5/gtsrb.zip) - German Traffic Sign Recognition Benchmark.

Overall, my models have the following structure, with slight differences in specific parameters:

1. Conv2D layer, ReLU activation
2. MaxPooling2D layer, 2x2 kernel
3. Conv2D layer, ReLU activation
4. MaxPooling2D layer, 2x2 kernel
5. Flatten layer
6. Dropout layer (0.5)
7. Hidden (dense) layer, ReLU activation
8. Output layer, SoftMax activation

Here are some models that I have trained and saved under the directory `models`:

| Version | Conv2D config1          | Conv2D config2          | Training accuracy | Testing accuracy | Hidden layer units | Comments                                |
|---------|-------------------------|-------------------------|-------------------|------------------|--------------------|-----------------------------------------|
| 1       | 64 filters, 3x3 kernel  | 64 filters, 3x3 kernel  | 0.9321            | 0.9632           | 64                 | Impressively good for the first try!    |
| 2       | 128 filters, 3x3 kernel | 128 filters, 3x3 kernel | 0.9358            | 0.9751           | 128                | Twice the parameter looks even better.  |
| 3       | 128 filters, 4x4 kernel | 256 filters, 2x2 kernel | 0.9538            | **0.9843**       | 128                | So far the best with some  fine-tuning! |
| 4       | 256 filters, 4x4 kernel | 256 filters, 2x2 kernel | 0.9269            | 0.9627           | 256                | Larger scale doesn't always make sense. |

It is worth mentioning that when constructing my first neural networks, I initially put the Dropout layer between the
Output layer and the Hidden layer (similar to the lecture source code), and then asked GPT for advice. However, GPT told
me that it is a common way to put Dropout layer **before** the Dense Layer rather than after it. I followed the advice
and found the effect surprisingly good, as shown above.

Later, I tried the original idea, with the same configuration with Version1 but swapping the order of the hidden layer
and dropout layer. The new model was saved as `models/v0.h5`. It turned out that the model is under-fitting in this
case, with a poor testing accuracy of 0.0550.
