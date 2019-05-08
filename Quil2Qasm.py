from Mappings import *

class QQConverter:

	def __init__(self, in_dir):
		self.handlers = get_handlers(self)

		self.qasm = []; self.qubits = 0
		with open(in_dir) as quil:
			for line in quil:
				self.process(line.split())

		if self.qubits:
			self.qasm.insert(0, 'qreg q[{}];'.format(self.qubits))

		# Adding preamble
		self.qasm.insert(0, 'include \"qelib1.inc\";')
		self.qasm.insert(0, 'OPENQASM 2.0;')

		print("\n~~~ QASM Output ~~~")
		print('\n'.join(self.qasm))

		out_dir = in_dir.replace('.quil', '.qasm')
		with open(out_dir, 'w') as f:
			f.write('\n'.join(self.qasm))

	def process(self, args):
		if args: 
			name = args[0].split('(')[0]
			self.handlers[name](*args)
		else: self.qasm.append('')

	##################
    # Command Handlers
	##################
	def simple_gate(self, name, *qs):
		"""
		Handles commands of the form `gatename q0 q1 ... qk`
		"""
		if name not in NAME_MAP: return
		qasm_line = NAME_MAP[name]
		for idx, q in enumerate(qs):
			end = ';' if idx == len(qs)-1 else ','
			qasm_line += ' q[{}]{}'.format(q, end)
		self.qasm.append(qasm_line)

		# Updates maximum qubit index
		max_q = max([int(q) for q in qs]) + 1
		if max_q > self.qubits:
			self.qubits = max_q

	def param_gate(self, id_, *qs):
		"""
		Handles commands of the form `gatename(param) q0 q1 ... qk`
		"""
		name = id_.split('(')[0]
		if name not in NAME_MAP: return
		qasm_line = id_.replace(name, NAME_MAP[name])
		for idx, q in enumerate(qs):
			end = ';' if idx == len(qs)-1 else ','
			qasm_line += ' q[{}]{}'.format(q, end)
		self.qasm.append(qasm_line)

		# Updates maximum qubit index
		max_q = max([int(q) for q in qs]) + 1
		if max_q > self.qubits:
			self.qubits = max_q

	# TODO: differentiate between memory types (REAL, OCTET, INTEGER)
	def declare(self, _, id_, mem):
		"""
		Handles `DECLARE id_ type[size]`
		"""
		size = ''.join(filter(str.isdigit, mem.split('[')[1]))
		qasm_line = 'creg {}[{}];'.format(id_, size)
		self.qasm.append(qasm_line)

	def measure(self, _, q, c):
		"""
		Handles `MEASURE q c`
		"""
		qasm_line = 'measure q[{}] -> {};'.format(q, c)
		self.qasm.append(qasm_line)

	def reset(self, _, idx=None):
		"""
		`RESET`: resets all qubits
		`RESET idx`: resets qubit `idx`
		"""
		if idx == None:
			for i in range(self.qubits):
				self.qasm.append('reset q[{}];'.format(i))
		else:
			self.qasm.append('reset q[{}];'.format(idx))

	def comment(self, *args):
		self.qasm.append(' '.join(args).replace('#', '//'))








if __name__ == '__main__':
	
	converter = QQConverter(in_dir = 'data/tests/hello_world.quil')