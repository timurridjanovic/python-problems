import unittest
from question3 import incr_dict

class Question3Tests(unittest.TestCase):
    def test_base_input(self):
        """
        testing base input
        """
        tpl = ('a', 'b', 'c')
        self.assertEqual(incr_dict({}, tpl), {'a': {'b': {'c': 1}}})

    def test_multiple_inputs(self):
        """
        testing multiple inputs
        """
        dct = {}
        incr_dict(dct, ('a', 'b', 'c'))
        incr_dict(dct, ('a', 'b', 'c'))
        incr_dict(dct, ('a', 'b', 'f'))
        incr_dict(dct, ('a', 'r', 'f'))
        incr_dict(dct, ('a', 'z'))
        self.assertEqual(dct, {'a': {'r': {'f': 1}, 'b': {'c': 2,'f': 1}, 'z': 1}})

    def test_multiple_inputs_2(self):
        """
        testing multiple inputs with tuples of variying lengths
        """
        dct = {}
        incr_dict(dct, ('a', 'b')) 
        incr_dict(dct, ('a', 'b', 'c', 'd', 'e'))
        incr_dict(dct, ('a', 'b', 'c', 'd', 'e'))
        incr_dict(dct, ('a', 'r', 'k', 'd', 'e'))
        incr_dict(dct, ('k', 'q'))
        incr_dict(dct, ('a', 'c'))
        self.assertEqual(dct, {'a': {'r': {'k': {'d': {'e': 1}}}, 'b': {'c': {'d': {'e': 2}}}, 
            'c': 1}, 'k': {'q': 1}})

    def test_large_input(self):
        """
        testing large input
        """
        dct = {}
        tpl = tuple([str(e) for e in range(1, 50)])
        result = {'1': {'2': {'3': {'4': {'5': {'6': {'7': {'8': {'9': {'10': 
            {'11': {'12': {'13': {'14': {'15': {'16': {'17': {'18': {'19': {'20': 
            {'21': {'22': {'23': {'24': {'25': {'26': {'27': {'28': {'29': {'30': 
            {'31': {'32': {'33': {'34': {'35': {'36': {'37': {'38': {'39': {'40': 
            {'41': {'42': {'43': {'44': {'45': {'46': {'47': {'48': {'49': 1}
            }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}

        incr_dict(dct, tpl)
        self.assertEqual(dct, result)

    def test_very_large_input(self):
        """
        testing very large input. Just checking 
        that the function doesn't throw an error
        """
        dct = {}
        tpl = tuple([str(e) for e in range(1, 100000)])
        try:
            incr_dict(dct, tpl)
        except ExceptionType:
            self.fail('incr_dict() raised ExceptionType unexpectedly')

    def test_empty_tuple(self):
        """
        testing function with an empty tuple
        """
        self.assertEqual(incr_dict({}, ()), {})

    def test_one_element_in_tuple(self):
        """
        testing function with len(tuple) == 1
        """
        self.assertEqual(incr_dict({'a': 1}, ('a',)), {'a': 2})

    def test_wrong_type_first_argument(self):
        """
        testing if function raises a TypeError if dct is of the wrong type
        """
        self.assertRaises(TypeError, incr_dict, 8 , ('a', 'b', 'c'))

    def test_wrong_type_second_argument(self):
        """
        testing if function raises a TypeError if tpl is of the wrong type
        """
        self.assertRaises(TypeError, incr_dict, {} , 'haha')



if __name__ == "__main__":
    unittest.main()
