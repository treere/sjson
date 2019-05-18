
class SJCallback:
    def start(self):
        pass

    def end(self):
        pass

    def start_object(self):
        pass

    def end_object(self):
        pass

    def start_list(self):
        pass

    def end_list(self):
        pass

    def obj_key(self, s: str):
        pass

    def obj_value_string(self, v: str):
        pass

    def obj_value_bool(self, b: bool):
        pass

    def obj_value_number(self, n : number):
        pass

    def obj_value_null(self):
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
                
        if c.isdigit() or c == "-":   # Parsing number
            if c == "-":
                d = 0
                sign = -1
            else:
                d = int(c)
                sign = 1
            div = 0
                
            while True:
                # TODO: \" is not managed
                c = stream.read(1)
                if c == '.':
                    if div != 0:
                        # TODO: exception double point
                        pass
                    div = 1
                elif not c.isdigit():
                    break
                elif len(c) == 0:
                    # TODO: error
                    pass
                else:
                    div *= 10
                    d = d*10 + int(c)

            div = 1 if div == 0 else div
            cb.obj_value_number(sign * d / div)

        # Not an elif because c could be changed
        if c == "{":               # Begin of dictionaries
            cb.start_object()
            side = False
        elif c == "}":               # End of dictionaries
            cb.end_object()
        elif c == "[":               # Begin of list
            cb.start_list()
        elif c == "]":               # End of list
            cb.end_list()
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
        elif c == 'n':               # Start of null
            c = stream.read(3)
            if c == 'ull':
                cb.obj_value_null()
            else:
                # TODO: error in parsing
                pass
        
        c = stream.read(1)
        
    cb.end()
        
