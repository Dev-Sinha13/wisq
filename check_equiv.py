#!/usr/bin/env python3

import sys
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator

def remove_measurements(circ: QuantumCircuit) -> QuantumCircuit:
    try:
        return circ.remove_final_measurements(inplace=False)
    except Exception:
        new = QuantumCircuit(circ.num_qubits)
        for inst, qargs, cargs in circ.data:
            if inst.name != "measure":
                new.append(inst, qargs, cargs)
        return new

def are_circuits_equivalent(qasm1, qasm2):
    circ1 = QuantumCircuit.from_qasm_file(qasm1)
    circ2 = QuantumCircuit.from_qasm_file(qasm2)

    c1_nom = remove_measurements(circ1)
    c2_nom = remove_measurements(circ2)

    c1_t = transpile(c1_nom, basis_gates=['u3','cx'])
    c2_t = transpile(c2_nom, basis_gates=['u3','cx'])

    op1 = Operator(c1_t)
    op2 = Operator(c2_t)

    return op1.equiv(op2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_equiv_operator_only.py file1.qasm file2.qasm")
        sys.exit(1)
    eq = are_circuits_equivalent(sys.argv[1], sys.argv[2])
    print("Equivalent" if eq else "NOT equivalent")
