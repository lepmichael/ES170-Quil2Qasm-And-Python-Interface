OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg ro[4];
h q[0];
measure q[0] -> ro[0];