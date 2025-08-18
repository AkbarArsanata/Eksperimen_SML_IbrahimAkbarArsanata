# 📚 Deep Learning Formula

Deep learning can be described mathematically as a **composition of functions**.

---

## 🔑 General Formula

For a neural network with **L layers**:

$$
\hat{y} = f(x; \theta) = f^{(L)}(f^{(L-1)}(\dots f^{(1)}(x)))
$$

- \(x\) = input data  
- \(\hat{y}\) = model prediction  
- \(\theta = \{W^{(1)}, b^{(1)}, \dots, W^{(L)}, b^{(L)}\}\) = weights and biases  

---

## 🔂 Forward Propagation

For each layer \(l\):

$$
z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}
$$

$$
a^{(l)} = \sigma^{(l)}(z^{(l)})
$$

- \(a^{(0)} = x\) (input layer)  
- \(z^{(l)}\) = linear transformation  
- \(\sigma^{(l)}\) = activation function (ReLU, sigmoid, tanh, etc.)  

---

## 🎯 Loss Function

To measure the error between true label \(y\) and prediction \(\hat{y}\):

- **Mean Squared Error (Regression):**

$$
\mathcal{L} = \frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2
$$

- **Cross-Entropy (Classification):**

$$
\mathcal{L} = - \sum_{i=1}^N y_i \log(\hat{y}_i)
$$

---

## 🔄 Backpropagation (Gradient Descent Update)

Update weights and biases:

$$
W^{(l)} \leftarrow W^{(l)} - \eta \frac{\partial \mathcal{L}}{\partial W^{(l)}}
$$

$$
b^{(l)} \leftarrow b^{(l)} - \eta \frac{\partial \mathcal{L}}{\partial b^{(l)}}
$$

- \(\eta\) = learning rate  
- Gradients computed using **chain rule**  

---

## ✅ Final Summary

The deep learning workflow can be summarized as:

$$
\hat{y} = f(x; \theta), \quad
\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}(y, f(x; \theta))
$$
