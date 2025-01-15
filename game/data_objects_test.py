import unittest
import game.data_objects as data_objects


class TestVector(unittest.TestCase):
    def test_vector_string_override(self):
        v = data_objects.Vector(x=3, y=9)
        expected = '<3, 9>'
        self.assertEqual(expected, v.__str__())


    def test_vector_equalities(self):
        self.assertEqual(
            data_objects.Vector(x=4, y=2),
            data_objects.Vector(x=4, y=2),
        )

        self.assertNotEqual(
            data_objects.Vector(x=5, y=2),
            data_objects.Vector(x=4, y=2),
        )


    def test_adding_vectors(self):
        expected = data_objects.Vector(4, 3)
        a = data_objects.Vector(1, 1)
        b = data_objects.Vector(3, 2)
        self.assertEqual(expected, data_objects.add_vectors(a, b))


if __name__ == '__main__':
    unittest.main()
