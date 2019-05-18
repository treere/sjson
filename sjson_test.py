import unittest
import uio
import sjson

class TestInit(unittest.TestCase):

    def test_start_callback_is_not_called(self):
        is_called = False
        def start():
            nonlocal is_called
            is_called = True
            
        data = uio.StringIO("")
        sjson.loads(data,start,None)
        
        self.assertFalse(is_called)

    def test_start_callback_is_called(self):
        is_called = False
        def start():
            nonlocal  is_called
            is_called = True
            
        data = uio.StringIO("ciao")
        sjson.loads(data,start,None)
        
        self.assertTrue(is_called)

    def test_end_callback_is_called_on_empty(self):
        is_called = False
        def end():
            nonlocal  is_called
            is_called = True
            
        data = uio.StringIO("")
        sjson.loads(data,None,end)
        
        self.assertTrue(is_called)

    def test_end_callback_is_called(self):
        is_called = False
        def end():
            nonlocal  is_called
            is_called = True
            
        data = uio.StringIO("ciao")
        sjson.loads(data,None,end)
        
        self.assertTrue(is_called)


if __name__ == '__main__':
    unittest.main()

