from evt import *

class InputEvt( Evt ) :
   def __init__(self) :
      super().__init__()
      self.input_nr = 0
