def input_text(filename):
	f = open(filename, "rb")
	input = f.read()
	f.close()
	return input

def indexForSymbol(dict, symb):
	j = 0
	for i in dict:
		if symb != i:
			j += 1
		else: return j + 2

def outPutBit(bit, out_file):	
	global write_bit
	global bit_len
	write_bit >>= 1
	if (bit & 1):
		write_bit |= 0x80
	bit_len -= 1
	if bit_len == 0:
		bit_len = 8
		out_file.write(write_bit.to_bytes(1, "little"))

def inPutBit(in_file):  
	global read_bit
	global bit_len
	global useless_bit
	if bit_len == 0:
		sid_bit = in_file.read(1)
		read_bit = int.from_bytes(sid_bit, "little")
		if sid_bit == b"":
			useless_bit += 1
			read_bit = 255
			if useless_bit > 14:
				exit(1)
		bit_len = 8

	t = read_bit & 1
	read_bit >>= 1
	bit_len -= 1
	return t

def bitPlusFollow(bit, bit_to_follow, out_file):	
	outPutBit(bit, out_file)
	for _ in range(bit_to_follow):
		outPutBit(~bit, out_file)

def coding(filename):

	global write_bit
	global bit_len
	bit_len = 8
	write_bit = 0

	txt = input_text(filename)	#считываем текст
	dictonary = {}
	for x in txt:
		dictonary[x] = dictonary.setdefault(x, 0) + 1

	sorted_dict = dict(sorted(dictonary.items(), key=lambda item: item[1], reverse=True))	#создаем словарь по тексту
	amount = len(sorted_dict)
	symb = list(sorted_dict.keys())
	val = list(sorted_dict.values())

	dict_mas = [0, 1]
	for i in sorted_dict:
		dict_mas.append(sorted_dict[i] + dict_mas[-1])

	with open(f"{filename}.arf", "wb+") as f:
		f.write(amount.to_bytes(1, "little"))	#записываем словарь
		for i in range(amount):
			f.write(symb[i].to_bytes(3, "little"))
			f.write(val[i].to_bytes(3, "little"))
		
		with open(filename, 'r') as fp:	#сжатие на целочисленных операциях
			l0 = 0
			h0 = (1<<16)-1  # 2^16 - 1 (65535)
			difference = h0 - l0 + 1
		
			delitel = dict_mas[-1]

			First_qtr = int(int(h0 + 1) / 4)	#16384
			Half = First_qtr * 2				#32768
			Third_qtr= First_qtr * 3			#49152
		
			bits_to_follow = 0		#сколько битов сбрасывать
		
			symbol = fp.read(1)		#читаем символ
			while symbol:
				j = indexForSymbol(sorted_dict, ord(symbol))	#находим индекс
				h0 = int(l0 + dict_mas[j] * difference / delitel - 1)
				l0 = int(l0 + dict_mas[j - 1] * difference / delitel)

				while True:	#обрабатываем варианты переполнения
					if h0 < Half:
						bitPlusFollow(0, bits_to_follow, f)
						bits_to_follow=0
					elif l0 >= Half:
						bitPlusFollow(1, bits_to_follow, f)
						bits_to_follow=0
						l0 -= Half
						h0 -= Half
					elif l0 >= First_qtr and h0 < Third_qtr:
						bits_to_follow += 1
						l0 -= First_qtr
						h0 -= First_qtr
					else:
						break
					l0 += l0
					h0 += h0 + 1

				difference = h0 - l0 + 1
				symbol = fp.read(1)

			h0 = int(l0 + dict_mas[1] * difference / delitel - 1)
			l0 = int(l0 + dict_mas[0] * difference / delitel)

			while True:
				if h0 < Half:
					bitPlusFollow(0, bits_to_follow, f)
					bits_to_follow=0
				elif l0 >= Half:
					bitPlusFollow(1, bits_to_follow, f)
					bits_to_follow=0
					l0 -= Half
					h0 -= Half
				elif l0 >= First_qtr and h0 < Third_qtr:
					bits_to_follow += 1
					l0 -= First_qtr
					h0 -= First_qtr
				else:
					break
				l0 += l0
				h0 += h0 + 1
			bits_to_follow += 1
			if l0 < First_qtr:
				bitPlusFollow(0, bits_to_follow, f)
				bits_to_follow=0
			else:
				bitPlusFollow(1, bits_to_follow, f)
				bits_to_follow=0

			write_bit >>= bit_len
			f.write(write_bit.to_bytes(1, "little"))

def decoding(filename):

	global read_bit
	global bit_len
	global useless_bit
	read_bit = 0
	bit_len = 0
	useless_bit = 0

	with open(filename, "rb") as f_in:

		b = f_in.read(1)
		amount_symb = int.from_bytes(b, 'little')
		dictonary = {}
		for x in range(amount_symb): #чтение словаря
			c = f_in.read(6)
			key = int.from_bytes(c[:len(c)//2], 'little')
			val = int.from_bytes(c[len(c)//2:], 'little')
			dictonary[key] = dictonary.setdefault(key, val)

		dict_mas = [0, 1]
		for i in dictonary:
			dict_mas.append(dictonary[i] + dict_mas[-1])

		with open(f"dec.{filename}", "wb+") as out:
			l0 = 0
			h0 = (1 << 16) - 1  # 2^16 - 1 (65535)
			difference = h0 - l0 + 1
			
			delitel = dict_mas[-1]
			
			First_qtr = int(int(h0 + 1) / 4)	#16384
			Half = First_qtr * 2				#32768
			Third_qtr = First_qtr * 3			#49152
			value = 0

			lst = list(dictonary.keys())

			for i in range(16):
				k = inPutBit(f_in)
				value += value + k
				
			while True:
				freq = int(((value - l0 + 1) * delitel - 1) / difference)
				j = 1
				while dict_mas[j] <= freq:	#поиск символа
					j += 1
				h0 = int(l0 + dict_mas[j] * difference / delitel - 1)
				l0 = int(l0 + dict_mas[j - 1] * difference / delitel)

				while True:	#обрабатываем варианты переполнения
					if h0 < Half:
						pass
					elif l0 >= Half:
						l0 -= Half
						h0 -= Half
						value -= Half
					elif l0 >= First_qtr and h0 < Third_qtr:
						l0 -= First_qtr
						h0 -= First_qtr
						value -= First_qtr
					else:
						break
					l0 += l0
					h0 += h0 + 1
					k = inPutBit(f_in)
					value += value + k
				if j == 1:
					break
				out.write(lst[j - 2].to_bytes(1, "little"))
				difference = h0 - l0 + 1

if __name__ == '__main__':

	print("[c]oding or [d]ecoding file?")
	type = input()

	print("Enter filename: ")
	file = input()

	if (type == "c"):
		coding(file)
		print("successfully!")
	elif (type == "d"):
		decoding(file)
		print("successfully!")
	else:
		print("Wrong action, pls, try again")
		exit(1)