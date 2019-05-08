OPENQASM 2.0;
include "qelib1.inc";
qreg q16[1];
creg c16[1];
x q16[0];
measure q16[0] -> c16[0];