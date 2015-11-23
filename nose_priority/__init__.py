import os
import json

def prioritize(args):

	


		# for test in newTests:
		# 	f = open(test[0].replace('.','/') + '.py', 'r')
		# 	contents = f.readlines()
		# 	f.close()
		# 	noImp = True
		# 	i = 0
		# 	for line in contents:
		# 		# Check for import statement
		# 		if "fromnose.plugins.attribimportattr" in line.translate(None, ' '):
		# 			noImp = False
		# 		if test[2] in line:
		# 			break
		# 		i += 1
		# 	while 1:
		# 		if len(contents[i]) == len(contents[i].lstrip()):
		# 			break
		# 		i -= 1
		# 	contents.insert(i-1, "\n@attr(priority='0')")
		# 	if noImp:
		# 		contents.insert(0, "\nfrom nose.plugins.attrib import attr")
		# 	f = open(test[0].replace('.','/') + '.py', 'w')
		# 	contents = "".join(contents)
		# 	f.write(contents)
		# 	f.close()

	# Add to test history
	if args['log']:
		# Add log to test history
		log = {'date' : '',
					'tests' : []
		}
		with open(args['log'], 'r') as f:
			date = None
			for line in f:
				if 'date' == line.rstrip('\n'):
					line = next(f)
					date = line.rstrip('\n')
					log['date'] = date
				if " ... " in line:
					linePieces = line.split(' ')
					newObject = {}
					newObject['test'] = linePieces[0]
					newObject['pass'] = linePieces[2]	
					log['tests'].append(newObject)
		data = None
		with open(os.path.dirname(__file__) + '/data.json', 'r') as f:
			data = json.load(f)
		with open(os.path.dirname(__file__) + '/data.json', 'w') as f:
			data.append(log)
			json.dump(data, f)


			# with open(os.path.dirname(__file__) + '/data.json', 'a') as f2:
			# 	json.dump(log, f2)

	# Import test history
	with open(os.path.dirname(__file__) + '/data.json', 'r') as f:
		data = json.load(f)
		print data
	# Set priorities
	if not args['ignore_new']:
		# Collect new tests 
		import subprocess
		import re
		p = subprocess.Popen(['nosetests', '--collect-only', '-v', '-a', '!priority'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		out, out2 = p.communicate()
		lines = out2.split('\n')
		newTests = []
		for line in lines:
			if line[-6:-3] == '...':
				testPath = line[:-7]
				test = testPath.rpartition('.')
				newTests.append(test)

		# Set new tests to priority=1
		for test in newTests:
			with open(test[0].replace('.','/') + '.py', 'a') as f:
				f.write('\n' + test[2] + '.priority = 1 # prioritize')