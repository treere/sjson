
def loads(stream: Stream , cb_start: Callback, cb_end: Callback):
    c = stream.read(1)
    if len(c) > 0 and cb_start:
        cb_start()

    if cb_end:
        cb_end()
        

