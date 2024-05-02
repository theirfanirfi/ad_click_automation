def read_input_data():
	try:
		f = open("inputs.txt", "r")
		data = f.read().splitlines()
		f.close()
		return data[0].split('\t')
	except Exception as e:
		print(e)
		return False

def write_input_data(data):
	f = open("inputs.txt", "w")
	f.write(data)
	f.close()


def write_keywords(keywords):
	f = open("keywords.txt", "w")
	f.write(keywords)
	f.close()

def read_keywords():
	f = open("keywords.txt", "r")
	data = f.read().splitlines()
	f.close()
	return data[0]

def read_account():
	f = open("account.txt", "r")
	data = f.read().splitlines()
	f.close()
	return data[0]

def write_account(account):
	f = open("account.txt", "w")
	f.write(account)
	f.close()