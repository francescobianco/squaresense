
from .gesture import GestureAnalyzer

class SquareSense:
	"""
	This class is used to define the protocol for the SquareSense device.
	It contains methods for sending and receiving data from the device.
	"""

	def __init__(self):
		self.analyzer = GestureAnalyzer()

	def input(self, data):
		"""
		Process the input data from the SquareSense device.

		:param data: The data to be processed.
		:return: None
		"""

		control_char = data[0]
		if control_char == '#':
			print("Comment: Ignoring line")
		elif control_char == '>':
			print("Received dataframe")
			print(f"Input data: {data}")
			cleaned_string = data[2:]
			hex_values = cleaned_string.strip().split()
			int_values = [int(h, 16) for h in hex_values]
			matrix_8x8 = [int_values[i:i+8] for i in range(0, 64, 8)]
			#for row in matrix_8x8:
			#	print(row)
			self.analyzer.update_board(matrix_8x8)

			self.analyzer.analyze()
			print(self.analyzer.get_status())



		else:
			print("Unknown command")





	def send_data(self, data):
		"""
		Send data to the SquareSense device.

		:param data: The data to be sent to the device.
		:return: None
		"""
		pass

	def receive_data(self):
		"""
		Receive data from the SquareSense device.

		:return: The data received from the device.
		"""
		pass