
class SJCallback:
    def start(self):
        pass

    def end(self):
        pass

    def start_object(self):
        pass

    def end_object(self):
        pass

    def obj_key(self, s: str):
        pass

    def obj_value_string(self, v: str):
        pass

def loads(stream: Stream , cb: SJCallback):
    c = stream.read(1)
    if len(c) > 0:
        cb.start()

    in_str = False
    side = False # False=left, True=right
    s = ""
    
    while True:
        if len(c) == 0:
            break

        if c == '"':
            if in_str:
                if side == False:
                    cb.obj_key(s)
                else:
                    cb.obj_value_string(s)
                s = ""
            in_str = not in_str
        elif in_str:
            s = s + c
        elif c == "{":
            cb.start_object()
            side = False
        elif c == "}":
            cb.end_object()
        elif c == ":":
            side = True
        elif c == ",":
            side = False
        

        c = stream.read(1)
        
    cb.end()
        
