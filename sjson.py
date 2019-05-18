
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
            if in_str and side == False:
                cb.obj_key(s)
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
        

        c = stream.read(1)
        
    cb.end()
        
