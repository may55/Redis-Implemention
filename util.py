# Print in case of error
def printSupportCmd():
	print('\033[1m' + '\033[91m' +"We support only following command" + '\033[0m')
	print("GET <key>")
	print("SET <key> <value>")
	print("EXPIRE <key>")
	print("ZADD <set> <score> <element>")
	print("ZRANK <set> <element>")
	print("ZRANGE <set> <start> <end>")
	print("EXIT - to exit and save the data in file.")

# supporting function
def splitInput(user_input):
	values = user_input.split('"')[1::2]
	cmd = user_input.split()[0]
	key = None
	if(len(user_input.split())>1):
		key = user_input.split()[1]
	return (cmd,key,values)