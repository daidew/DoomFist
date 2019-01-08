
import pyautogui as pg
import predictor
import threading



#make it not log silly thing
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#prepare data
data = predictor.data()
process = predictor.processor(data)

from flask import Flask, request

app = Flask(__name__)


# def getVal(sensor):
# 	global message
# 	print(message)
# 	if sensor == 'UP':
# 		return message[0]
# 	elif sensor == 'DOWN':
# 		return message[1]
# 	elif sensor == 'LEFT':
# 		return message[2]
# 	elif sensor == 'RIGHT':
# 		return message[3] 

# def moveMouseRel(xOffset, yOffset):
#         ctypes.windll.user32.mouse_event(0x0001, xOffset, yOffset, 0, 0)

# def job1(*message):
# 	global speed
# 	xspd = 0
# 	yspd = 0
# 	if(message[0] == '1'):
# 		yspd = -speed
# 	if(message[1] == '1'):
# 		yspd = speed
# 	if(message[2] == '1'):
# 		xspd = -speed
# 	if(message[3] == '1'):
# 		xspd = speed
# 	if(message[4] == '1'):
# 		pg.typewrite(['e'])
# 	moveMouseRel(xspd,yspd)

# def job2(*val):
# 	for i in val:
# 		print(i)



def printGet(Ax,Ay,Az,Gx,Gy,Gz,Touch,B1):
	print(locals())

def getHttp(Ax,Ay,Az,Gx,Gy,Gz,Touch,b1,up,down,left,right):
	data.update(Ax,Ay,Az,Gx,Gy,Gz,Touch,b1,up,down,left,right)
	process.update()




@app.route("/")
def __main__():
	# thread = threading.Thread(target = getHttp, kwargs = {'Ax' : request.args.get('Ax'), 'Ay' : request.args.get('Ay'), 'Az' : request.args.get('Az')
	# 	,'Gx' : request.args.get('Gx'), 'Gy' : request.args.get('Gy'), 'Gz' : request.args.get('Gz')
	# 	, 'Touch' : request.args.get('Touch'), 'b1' : request.args.get('B1')
	# 	,'up' : request.args.get('up'),'down' : request.args.get('down'),'left' : request.args.get('left'),'right' : request.args.get('right')})
	
	# thread.start()
	# thread.join()
	getHttp(request.args.get('Ax'),request.args.get('Ay'),request.args.get('Az')
		,request.args.get('Gx'),request.args.get('Gy'),request.args.get('Gz')
		,request.args.get('Touch'),request.args.get('B1')
		,request.args.get('up'),request.args.get('down'),request.args.get('left'),request.args.get('right'))


	return ''





# @app.route("/fuck")
# def __main2__():
# 	return "fuck"

app.run(host = '0.0.0.0',debug = True)
