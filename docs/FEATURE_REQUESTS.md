# Requesting Features

We love hearing about new feature ideas!

- **Open a GitHub Issue**: [https://github.com/qpiai/quantum-sdk/issues](https://github.com/qpiai/quantum-sdk/issues)
- **Email us**: support@qcloud.qpiai.tech
- **Include**:
  - Clear description of the proposed feature
  - Use case or problem it solves
  - Example code showing how you'd like to use it
  - Any relevant research papers or references

**Example Feature Request:**
````
Subject: Feature Request - Support for custom parametric gates

Description:
Add support for defining custom parametric quantum gates with symbolic parameters.

Use Case:
Implementing variational quantum algorithms requires gates with trainable parameters.

Proposed API:
```python
from qpiai_quantum import Circuit
circuit = Circuit(2, 2)
circuit.rx(0, theta=0.5)   # RX rotation gate
circuit.ry(1, theta=0.3)   # RY rotation gate
```
````
