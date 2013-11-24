
def read_named_int(text, name, delimiter = "\"") :
   return int(read_named_string(text, name, delimiter))

def read_named_float(text, name, delimiter = "\"") :
   return float(read_named_string(text, name, delimiter))

def read_named_string(text, name, delimiter = "\"") :
   if not name in text :
      return ""
   return text.split(name)[1].split(delimiter)[1]
