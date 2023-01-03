import os

def file_presence(file):	#проверяем файл на наличие
	filepath = os.path.join(file)
	return os.path.isfile(filepath)


def input_file(file):
	f = open(file, 'r')
	input = f.read()
	f.close()
	return input


def symbols_counter(file_in):
	if not(file_presence(file_in)): 
		print("File not found")
		exit(1)
	dictonary_price = 0
	with open(f"{file_in}", 'r') as file:
		piece = file.read(1)
		dictonary = {}
		while piece:
			if dictonary.get(piece) == None:
				dictonary.update({piece: 1})
			else:
				dictonary[piece] = dictonary[piece] + 1
			piece = file.read(1)
		for _, val in dictonary.items():
			dictonary_price += val
	sorted_slovar = dict(sorted(dictonary.items(), key=lambda item: item[1], reverse=True))
	return sorted_slovar


if __name__ == '__main__':

	print(input_file("text.txt"))
	
	print(symbols_counter("text.txt"))
	#print(file_presence("text.txt"))