import unittest
import uio
import sjson

class TestSJson(unittest.TestCase):
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
        start = TestSJson.Start()
        data = uio.StringIO("")

        sjson.loads(data,start)

        self.assertFalse(start.is_called)

    def test_start_callback_is_called(self):
        start = TestSJson.Start()

        data = uio.StringIO("ciao")        
        sjson.loads(data,start)

        self.assertTrue(start.is_called)

    def test_end_callback_is_called_on_empty(self):
        end = TestSJson.End()
            
        data = uio.StringIO("")
        sjson.loads(data,end)
        
        self.assertTrue(end.is_called)

    def test_end_callback_is_called(self):
        end = TestSJson.End()
            
        data = uio.StringIO("ciao")
        sjson.loads(data,end)
        
        self.assertTrue(end.is_called)


    class JObject(sjson.SJCallback):
        def __init__(self):
            self.is_start_called = False
            self.is_end_called = False

        def start_object(self):
            self.is_start_called = True

        def end_object(self):
            self.is_end_called = True

    def test_object_no_obj(self):
        obj = TestSJson.JObject()

        data = uio.StringIO("ciao")
        sjson.loads(data, obj)

        self.assertFalse(obj.is_start_called)
        self.assertFalse(obj.is_end_called)

    def test_object(self):
        obj = TestSJson.JObject()

        data = uio.StringIO('{"ciao"}')
        sjson.loads(data, obj)

        self.assertTrue(obj.is_start_called)
        self.assertTrue(obj.is_end_called)

    class JObjectKey(sjson.SJCallback):
        def __init__(self):
            self.last_key = None
            self.last_string = None

        def obj_key(self, key):
            self.last_key = key

        def obj_value_string(self, s):
            self.last_string = s

            
    def test_object_key(self):
        obj = TestSJson.JObjectKey()

        data = uio.StringIO('{"key":True}')
        sjson.loads(data, obj)

        self.assertEqual(obj.last_key,"key")

    def test_object_key_with_value_sting(self):
        obj = TestSJson.JObjectKey()

        data = uio.StringIO('{"key":"value"}')
        sjson.loads(data, obj)

        self.assertEqual(obj.last_key, "key")
        self.assertEqual(obj.last_string, "value")

    def test_object_with_two_string_keys(self):
        obj = TestSJson.JObjectKey()

        data = uio.StringIO('{"key1":"value1", "key2": "value2"}')
        sjson.loads(data, obj)

        self.assertEqual(obj.last_key, "key2")
        self.assertEqual(obj.last_string, "value2")

    class JBoolObject(sjson.SJCallback):
        def __init__(self):
            self.last_bool = None
        def obj_value_bool(self, b: bool):
            self.last_bool = b
            
    def test_object_with_a_boolean_True(self):
        obj = TestSJson.JBoolObject()

        data = uio.StringIO('{"key":true}')
        sjson.loads(data, obj)

        self.assertEqual(obj.last_bool, True)
        
    def test_object_with_a_boolean_False(self):
        obj = TestSJson.JBoolObject()

        data = uio.StringIO('{"key":false}')
        sjson.loads(data, obj)

        self.assertEqual(obj.last_bool, False)


    class JNumObject(sjson.SJCallback):
        def __init__(self):
            self.last_number = None
            self.ends = False

        def obj_value_number(self, n):
            self.last_number = n

        def end_object(self):
            self.ends = True
            
    def test_object_with_a_positive_integer(self):
        num = TestSJson.JNumObject()

        data = uio.StringIO('{"key":42}')
        sjson.loads(data, num)
        self.assertEqual(num.last_number, 42)
        self.assertTrue(num.end)

    def test_object_with_a_negative_integer(self):
        num = TestSJson.JNumObject()

        data = uio.StringIO('{"key":-42}')
        sjson.loads(data, num)
        self.assertEqual(num.last_number, -42)
        self.assertTrue(num.end)

if __name__ == '__main__':
    unittest.main()

