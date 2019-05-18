import unittest
import uio
import sjson

class TestInit(unittest.TestCase):
    class Start(sjson.SJCallback):
        def __init__(self):
            self.is_called = False
        def start(self):
            self.is_called = True

    class End(sjson.SJCallback):    
        def __init__(self):
            self.is_called = False
        def end(self):
            self.is_called = True

    def test_start_callback_is_not_called(self):    
        start = TestInit.Start()
        data = uio.StringIO("")

        sjson.loads(data,start)

        self.assertFalse(start.is_called)

    def test_start_callback_is_called(self):
        start = TestInit.Start()

        data = uio.StringIO("ciao")        
        sjson.loads(data,start)

        self.assertTrue(start.is_called)

    def test_end_callback_is_called_on_empty(self):
        end = TestInit.End()
            
        data = uio.StringIO("")
        sjson.loads(data,end)
        
        self.assertTrue(end.is_called)

    def test_end_callback_is_called(self):
        end = TestInit.End()
            
        data = uio.StringIO("ciao")
        sjson.loads(data,end)
        
        self.assertTrue(end.is_called)


if __name__ == '__main__':
    unittest.main()

