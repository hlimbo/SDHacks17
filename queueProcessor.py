# create a function that accepts a queue object of messages send via text
import queue

# lower values are higher priority in pq in python
# driftingbottles is queue that holds a collection of tuples
def processQueue(driftingbottles):

	print("hi")
	try:
		print("a")		
		fromData = driftingbottles.get_nowait()
		print("b")
		print("fromData ",fromData)
	except:
		print("no messages in queue")
		pass	

	print("bye")		
	# return 2 queues, 1st queue drifting bottles queue, 2nd queue of the users
	#return driftingbottles
