
class SJCallback:
    def start(self):
        pass

    def end(self):
        pass

    def start_object(self):
        pass

def loads(stream: Stream , cb: SJCallback):
    c = stream.read(1)
    if len(c) > 0:
        cb.start()

    while True:
        if len(c) == 0:
            break
        
        if c == "{":
            cb.start_object()
        elif c == "}":
            cb.end_object()

        c = stream.read(1)
        
    cb.end()
        
