
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

    def obj_value_bool(self, b: bool):
        pass


def loads(stream: Stream , cb: SJCallback):
    c = stream.read(1)
    if len(c) > 0:
        cb.start()

    side = False # False=left, True=right
    
    while True:
        if len(c) == 0:
            break

        if c == '"':  # Begin of a string
            s = ""
            while True:
                # TODO: \" is not managed
                c = stream.read(1)
                if c == '"':
                    break
                elif len(c) == 0:
                    # TODO: error
                    pass
                else:
                    s = s + c
                    
            if side == False:
                cb.obj_key(s)
            else:
                cb.obj_value_string(s)
        elif c == "{":               # Begin of dictionaries
            cb.start_object()
            side = False
        elif c == "}":
            cb.end_object()
        elif c == ":":                # Separator of dictionaries
            side = True
        elif c == ",":
            side = False
        elif c == 't':                # Start of True
            c = stream.read(3)
            if c == 'rue':
                cb.obj_value_bool(True)
            else:
                # TODO: error in parsing
                pass

        elif c == 'f':               # Start of False
            c = stream.read(4)
            if c == 'alse':
                cb.obj_value_bool(False)
            else:
                # TODO: error in parsing
                pass
        

        c = stream.read(1)
        
    cb.end()
        
