import os
global write_bit
global bit_len

write_bit = 0
bit_len = 8

def file_presence(file):	#проверяем файл на наличие
	filepath = os.path.join(file)
	return os.path.isfile(filepath)

def input_file(file_in):
	f = open(f"{file_in}", 'r')
	input = f.read()
	f.close()
	return input

def symbols_counter(file_in):
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
	sorted_dictonary = dict(sorted(dictonary.items(), key=lambda item: item[1], reverse=True))
	return sorted_dictonary

def symbol_index(dict_symb, argument):
	j = 0
	for i in dict_symb:
		if argument != i:
			j += 1
		else:
			j += 2
			return j

def bit_out(bit, file_out):		#подсмотрел в интернете
    global write_bit
    global bit_len
    write_bit >>= 1
    if bit & 1:
        write_bit |= 0x80
    bit_len -= 1
    if bit_len == 0:
        bit_len = 8
        file_out.write(write_bit.to_bytes(1, "little"))

def bit_add_follow(bit, next_bit, file_out):	#подсмотрел в интернете
    bit_out(bit, file_out)
    for _ in range(next_bit):
        bit_out(~bit, file_out)

def add_bit(low_value, high_value, next_bit, first_quality, half_quality, third_quality):
	out_file = open("out_text.txt", "wb+")
	if low_value >= half_quality:
		bit_add_follow(1, next_bit, out_file)
		next_bit=0
		low_value -= half_quality
		high_value -= half_quality
	elif high_value < half_quality:
		bit_add_follow(0, next_bit, out_file)
		next_bit=0
	elif low_value >= first_quality and high_value < third_quality:
		next_bit += 1
		low_value -= first_quality
		high_value -= first_quality
	else:
		return False
		
	low_value += low_value
	high_value += high_value + 1

def symbol_value(file_in, dict_symb):	#некоторые моменты были подсмотрены из псевдокода в итернете
	global write_bit
	global bit_len
	out_file = open("out_text.txt", "wb+")

	symb_mas = [0, 1]
	for i in dict_symb:
		symb_mas.append(dict_symb[i] + symb_mas[-1])
	
	with open(f"{file_in}", 'r') as file:
		low_value = 0
		high_value = (1<<16)-1  
		remover = symb_mas[-1]
		difference = high_value - low_value + 1
		first_quality = int(int(high_value + 1) / 4)
		half_quality = first_quality * 2
		third_quality = first_quality * 3
		next_bit = 0

		peace = file.read(1)
		while peace:
			j = symbol_index(dict_symb, peace)
			high_value = int(low_value + symb_mas[j] * difference / remover - 1)
			low_value = int(low_value + symb_mas[j - 1] * difference / remover)

			while True:
				add_bit(low_value, high_value, next_bit, first_quality, half_quality, third_quality)

			difference = high_value + 1 - low_value
			peace = file.read(1)

		high_value = int(low_value + symb_mas[1] * difference / remover - 1)
		low_value = int(low_value + symb_mas[0] * difference / remover)

		while True:
				add_bit(low_value, high_value, next_bit, first_quality, half_quality, third_quality)

		next_bit += 1
		if low_value < first_quality:
			bit_add_follow(0, next_bit, out_file)
			next_bit = 0
		else:
			bit_add_follow(1, next_bit, out_file)
			next_bit = 0

		write_bit >>= bit_len
		out_file.write(write_bit.to_bytes(1, "little"))
		
	out_file.close()	

def write_header(file_out, dict_symb):
	file = open(f"{file_out}", "wb+")
	file.write(len(dict_symb).to_bytes(1, "little"))
	for i in dict_symb:
		file.write(i.encode("ascii"))
		file.write(dict_symb[i].to_bytes(4, "little"))
	
def coding(file_in, file_out):
	dict_symb = symbols_counter(file_in)
	write_header(file_out, dict_symb)
	symbol_value(file_in, dict_symb)

def decoding():
	print("Hello")
	
if __name__ == '__main__':

	print("[c]oding or [d]ecoding file? ◕‿◕")
	arg1 = input()

	if not(arg1 == "c" or arg1 == "d"):	
		print("The parameter is set incorrectly! ¯\_(ツ)_/¯")
		exit(1)
		
	print("Enter file for coding.")
	print("For example: text.txt")
	arg2 = input()

	print("Enter file for decoding.")
	print("For example: out_text.txt")
	arg3 = input()
	
	if not(file_presence(arg2) or file_presence(arg3)): 
		print("Input or Out file was not found! ¯\_(ツ)_/¯")
		exit(1)

	if (arg1 == "c"):
		coding(arg2, arg3)
		print("File was successfully compressed!  \ (•◡•) /")
	elif (arg1 == "d"):
		decoding()
		print("File was successfully decompressed!  \ (•◡•) /")
		
