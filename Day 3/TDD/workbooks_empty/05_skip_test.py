import sys
import pytest
import unittest

@pytest.mark.skip(reason="This feature is not implemented yet.")
@pytest.mark.order(4)
def test_skip_functon():
    assert False

@pytest.mark.skipif(sys.platform == "win32", reason="This is not for windows :))")
@pytest.mark.order(1)
def test_no_windows():
    assert False

@pytest.mark.skipif(sys.version_info < (3, 13), reason="Python too old!?!?")
@pytest.mark.order(2)
def test_multiply():
    assert 5 == 5, "ye"

@pytest.mark.xfail(reason='this should fail :))')
@pytest.mark.order(3)
def test_some_error():
    assert False


class TestSkipsAndXFails(unittest.TestCase):

    @unittest.skip("This feature is not implemented yet.")
    def test_01_skip_functon(self):
        assert False

    @unittest.expectedFailure
    def test_some_error(self):
        assert False

    @unittest.skipIf(sys.platform == "win32", "This is not for windows")
    def test_no_windows(self):
        assert False

    @unittest.skipIf(sys.version_info < (3, 13), "old python, upgrade")
    def test_multiply(self):
        assert False


if __name__ == "__main__":
    unittest.main()
