# Reporting Bugs

If you encounter a bug or unexpected behavior:

- **Open a GitHub Issue**: [https://github.com/qpiai/quantum-sdk/issues](https://github.com/qpiai/quantum-sdk/issues)
- **Email us**: support@qcloud.qpiai.tech
- **Provide details**:
  - Python version and operating system
  - QpiAI Quantum SDK version (`import qpiai_quantum; print(qpiai_quantum.__version__)`)
  - Minimal code example that reproduces the issue
  - Full error message and traceback
  - Expected vs. actual behavior

**Example Bug Report:**
````
Subject: Bug Report - Circuit measurement error with multiple classical registers

Python: 3.10.8
OS: Ubuntu 22.04
SDK Version: 0.1.32

Description:
When measuring qubits into separate classical registers, the results are incorrect.

Code to reproduce:
```python
from qpiai_quantum import Circuit
circuit = Circuit(2, 2)
circuit.h(0)
circuit.measure([0], [0])
# Error occurs here...
```

Error message:
[Include full traceback]
````
