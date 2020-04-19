import datetime
import pickle
import re
import sys

#local import
from avl import ZNode, Tree
from util import printSupportCmd, splitInput



# The main redis
redis = dict()
'''
Definition of dictionary redis

redis{
	type : 0(STRING),1(SET)
	time : EXPIRE_TIME
	value : values
	set : dict()
	root : root
	tree : avl_tree_obj
}
'''


f = open('file.pkl','rb')

# Loading old data from file
try:
	for i in range(1):
		redis = pickle.load(f)
except:
	redis = dict()

f.close()

last_time = datetime.datetime.now()


while(True):
	try:
		user_input = input()

		# Splitting the input
		(cmd,key,values) = splitInput(user_input)

		# SET Command
		if(cmd == "SET"):
			redis[key] = dict()
			redis[key]['type'] = 0
			redis[key]['time'] = datetime.datetime.max
			redis[key]['value'] = values[0]
			redis[key]['set'] = None
			redis[key]['root'] = None
			redis[key]['tree'] = None
			print('OK')

		# GET Command
		elif(cmd == "GET"):
			if key in redis:
				if(redis[key]['type'] != 0):
					print('(error) WRONGTYPE Operation against a key holding the wrong kind of value')
				elif(redis[key]['time']>=datetime.datetime.now()):
					print(redis[key]['value'])
				else:
					# Key is expired
					del redis[key]
					print('(nil)')
			else:
				print('(nil)')

		# EXPIRE Command
		elif(cmd=="EXPIRE"):
			if key in redis:
				delta = datetime.timedelta(seconds=int(user_input.split()[2]))	
				redis[key]['time'] = datetime.datetime.now()+delta
				print(1)
			else:
				print(0)

		# ZADD Command
		elif(cmd=="ZADD"):
			cmd_spl = user_input.split()[2:]
			count = 0
			valid_cmd = (len(cmd_spl)%2)==0
			if(not valid_cmd):
				print("(error) ERR syntax error")
				continue
			for i in range(0,len(cmd_spl),2):
				try:
					score = float(cmd_spl[i])
				except:
					valid_cmd = False
					break
			if(not valid_cmd):
				print("(error) ERR syntax error")
				continue

			for i in range(0,len(cmd_spl),2):
				element = cmd_spl[i+1][1:-2]
				score = float(cmd_spl[i])
				if key in redis:
					if(redis[key]['type']==0 and redis[key]['time']>=datetime.datetime.now()):
						print("(error) WRONGTYPE Operation against a key holding the wrong kind of value")

					#if the set was expired
					elif(redis[key]['time']<datetime.datetime.now()):
						redis[key]['type'] = 1
						redis[key]['time'] = datetime.datetime.max
						redis[key]['value'] = None
						redis[key]['set'] = dict()
						redis[key]['root'] = None
						redis[key]['tree'] = Tree()
						redis[key]['root'] = redis[key]['tree'].insert(redis[key]['root'],
																				score,element,None,None)
						if(redis[key]['set'] is None):
							redis[key]['set'] = dict()
						redis[key]['set'][element] = score
						count += 1
					else:
						if(redis[key]['set']!=None and element in redis[key]['set']):
							#delete last copy
							redis[key]['root'] = redis[key]['tree'].delete(redis[key]['root'],
																			redis[key]['set'][element],
																			element, None, None)
							#insert new copy
							redis[key]['root'] = redis[key]['tree'].insert(redis[key]['root'],
																			score,element,None,None)
							redis[key]['set'][element] = score
							# print(0)

						else:
							redis[key]['root'] = redis[key]['tree'].insert(redis[key]['root'],
																			score,element,None,None)
							if(redis[key]['set'] is None):
								redis[key]['set'] = dict()
							redis[key]['set'][element] = score
							count += 1
						
				else:
					redis[key] = dict()
					redis[key]['type'] = 1
					redis[key]['time'] = datetime.datetime.max
					redis[key]['value'] = None
					redis[key]['set'] = dict()
					redis[key]['root'] = None
					redis[key]['tree'] = Tree()
					redis[key]['root'] = redis[key]['tree'].insert(redis[key]['root'],
																			score,element,None,None)
					redis[key]['set'][element] = score
					count += 1
			print(count)

		# ZRANK Command
		elif(cmd=="ZRANK"):
			element = values[0]
			if(key in redis):
				if(redis[key]['type']==0):
					print("(error) WRONGTYPE Operation against a key holding the wrong kind of value")
				elif(redis[key]['set']!=None and element in redis[key]['set']):
					score = redis[key]['set'][element]
					idx = redis[key]['tree'].getRank(redis[key]['root'],score,element)
					if(idx==-1):
						del redis[key]['set'][element]
						print("Element doesn't exist.")
					else:	
						print(idx)
				else:
					print("Element doesn't exist.")
			else:
				print("Set doesn't exist.")

		# ZRANGE Command
		elif(cmd=="ZRANGE"):
			start = int(user_input.split()[2])
			end = int(user_input.split()[3])
			with_score = False
			if user_input.split()[-1]== "WITHSCORES":
				with_score = True
			if(key in redis):
				if(redis[key]['type']==0):
					print("(error) WRONGTYPE Operation against a key holding the wrong kind of value")
				
				n_element = redis[key]['root'].n_count # Total element in the set
				if(start<0):
					start = start%n_element
				if(end<0):
					end = end%n_element
				start = min(n_element,start)
				end = min(n_element,end)
				if(start>end):
					print("(empty list or set)")
				else:
					elements = redis[key]['tree'].getRange(redis[key]['root'],start,end)
					if(len(elements)==0):
						print("(empty list or set)")
					for element in elements:
						print(element.element)
						if(with_score):
							print(element.score)
			else:
				print("(empty list or set)")

		elif(cmd=="EXIT"):
			break
		else:
			printSupportCmd()

		delta = datetime.timedelta(seconds=60)	
		if(last_time+delta>datetime.datetime.now()):
			f = open('file.pkl','wb')
			pickle.dump(redis,f)
			f.close()
			last_time = datetime.datetime.now()

	except :
		print("Unexpected error:", sys.exc_info())
		printSupportCmd()
		print('\033[1m' + '\033[91m' +"(Bad Query)Some argument missing in your cammand" + '\033[0m')



f = open('file.pkl','wb')
pickle.dump(redis,f)
f.close()