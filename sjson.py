
class SJCallback:
    def start(self):
        pass

    def end(self):
        pass

def loads(stream: Stream , cb: SJCallback):
    c = stream.read(1)
    if len(c) > 0:
        cb.start()
    cb.end()
        
