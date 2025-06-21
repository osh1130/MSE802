# In this code, I follow the oracle construction style provided by the instructor,
# where the oracle is represented as a unitary matrix. While the sample code used
# an identity matrix (i.e., no hidden structure), here I implement a *periodic* oracle
# for Simon's problem, specifically encoding a period of '10' (in binary).

# The main tasks performed are:
# - Constructing the oracle matrix for a function f(x) with hidden period 10,
#   following the same matrix-gate approach as in the instructor's example.
# - Building a 4-qubit quantum circuit using Cirq: Hadamard gates on the first two
#   qubits, applying the oracle gate, Hadamard gates again, and measuring the x register.
# - Running the quantum circuit multiple times and collecting the measurement results.

# Main conclusion:
# - Unlike the identity oracle, which shows no structure in the measurement results,
#   the periodic oracle leads to measurement outcomes that satisfy the equation z·c=0,
#   where c is the hidden period. This confirms that Simon's algorithm can reveal
#   the period from the measurement statistics when the oracle encodes a periodic function.

import cirq
import numpy as np
from collections import Counter
import itertools

# Build the 16x16 oracle matrix for the function with period 10
def f(x):
    lookup = {
        0b00: 0b01,
        0b01: 0b10,
        0b10: 0b01,
        0b11: 0b10
    }
    return lookup[x]

oracle_matrix = np.zeros((16, 16), dtype=float)
for x, y in itertools.product(range(4), range(4)):
    input_index = (x << 2) | y
    output_index = (x << 2) | (y ^ f(x))
    oracle_matrix[output_index, input_index] = 1

# Create the oracle gate from the unitary matrix
oracle_gate = cirq.MatrixGate(oracle_matrix)

# Define the quantum circuit
def simon_circuit(oracle_gate):
    # Define four qubits
    qubits = cirq.LineQubit.range(4)
    # Create a quantum circuit
    circuit = cirq.Circuit()
    # Apply Hadamard gate to the first two qubits
    circuit.append([cirq.H(qubits[i]) for i in range(2)])
    # Apply the oracle gate
    circuit.append(oracle_gate(*qubits))
    # Apply Hadamard gate to the first two qubits
    circuit.append([cirq.H(qubits[i]) for i in range(2)])
    # Measure the first two qubits
    circuit.append([cirq.measure(qubits[i], key=f'result_{i}') for i in range(2)])
    return circuit

# Create the quantum circuit with the oracle gate
circuit = simon_circuit(oracle_gate)
# Simulate the circuit 100 times
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=100)

# Collect the measurement results
measurements = result.measurements
counts = Counter(tuple(measurements[f'result_{i}'][j][0] for i in range(2)) for j in range(100))

# Print the measurement results
print("Measurement results (bitstring: frequency):")
for outcome, frequency in counts.items():
    print(f"{outcome}: {frequency}")

# Print the circuit
print("\nCircuit:")
print(circuit)
