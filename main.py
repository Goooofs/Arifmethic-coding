import os
global write_bit
global bit_len

write_bit = 0
bit_len = 8

def file_presence(file):	#проверяем файл на наличие
	filepath = os.path.join(file)
	return os.path.isfile(filepath)


def input_file(file_in):
	f = open(f"{file_in}", 'r', encoding='utf-8')
	input = f.read()
	f.close()
	return input


def symbols_counter(file_in):
	if not(file_presence(file_in)): 
		print("File not found")
		exit(1)
	dictonary_price = 0
	with open(f"{file_in}", 'r', encoding='utf-8') as file:
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

def price(dict_symb):
	total_price = 0
	for i in dict_symb:
		total_price += dict.get(dict_symb, i)
	dictonary = dict.copy(dict_symb)
	for x in dictonary:
		price_symb = dict.get(dict_symb, i) / total_price #под вопросом,скорее всего переделаю
		dictonary.update(price_symb)
		print(dictonary)


def Symbol_index(dict_symb, argument):
	j = 0
	for i in dict_symb:
		if argument != i:
			j += 1
		else:
			j += 2
			return j

def bit_out(bit, file_out):
    global write_bit
    global bit_len
    write_bit >>= 1
    if bit & 1:
        write_bit |= 0x80
    bit_len -= 1
    if bit_len == 0:
        bit_len = 8
        file_out.write(write_bit.to_bytes(1, "little"))

def bit_add_follow(bit, next_bit, file_out):
    bit_out(bit, file_out)
    for _ in range(next_bit):
        bit_out(~bit, file_out)
		
if __name__ == '__main__':

	print(input_file("text.txt"))
	
	print(symbols_counter("text.txt"))
	#print(file_presence("text.txt"))

	dict_symb = symbols_counter("text.txt")

#dict.get(key[, default])
#ert = dict.get(dict_sym, 'a')
#print(ert)
#price(dict_symb)

slovar_mas = [0, 1]
for i in dict_symb:
    slovar_mas.append(dict_symb[i] + slovar_mas[-1])

