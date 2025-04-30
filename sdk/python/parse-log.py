

from .squaresense import SquareSense

if __name__ == "__main__":

	squaresense = SquareSense()

	print("Running as a script")
	file = "fixtures/dataset/synthetic/e2e4.log"
	with open(file, "r") as f:
		lines = f.readlines()
		for line in lines:
			squaresense.input(line.strip())
