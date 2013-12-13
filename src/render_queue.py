from billboard import *

rq = []
def enqueue(b) :
   rq.append(b)
   if hasattr(b, "containers") :
      b.containers.append(rq)

def dequeue(b) :
   if b in rq :
      rq.remove(b)

def render() :
   for b in rq :
      b.render()
