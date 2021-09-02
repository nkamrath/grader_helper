
logs = []
current_print_level = 1
LOG_LEVEL_ALWAYS_PRINT = 0
LOG_LEVEL_ERROR = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_INFO = 3
LOG_LEVEL_DEBUG = 4

def set_print_level(level):
	global current_print_level 
	current_print_level= level

def log(*message, level = LOG_LEVEL_INFO):
	global logs
	global current_print_level
	while(len(logs) <= level):
		logs.append([])
	temp = ""
	for arg in message:
		temp += str(arg)
	logs[level].append(temp)
	if(level <= current_print_level):
		print(temp)

def log_show():
	print("logs:")
	global logs
	for log_level in logs:
		print("")
		for l in log_level:
			print(l)
