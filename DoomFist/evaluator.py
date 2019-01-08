s = [list() for i in range(120)]
u = [list() for i in range(120)]
c = [list() for i in range(120)]



slm_c = lambda e: e['ay'] < -1.9
uppc_c =  lambda e: False
chrg_init_c = lambda e: True
chrg_rel_c = lambda e: True

end = ''
def evaluate(list,c):
	no = set()
	n = sum(1 for subList in list if len(subList) > 0)
	print("how many data set",n)
	for idx,rev in enumerate(list):
		if idx >= n: break
		if all((not c(e)) for e in rev):
			no.add(idx)
	print("how many data set that can't detect",len(s))
def clearlist():
	l = [list() for i in range(120)]


def evaluate_all(ls,lu,lchrg):
	list = [ls,lu,lchrg]
	for data in list:
		print("by slam condition")
		evaluate(data,slm_c)
		print("by uppercut condition")
		evaluate(data,uppc_c)
		print("by charge condition")
		evaluate(data,chrg_init_c)
	
	