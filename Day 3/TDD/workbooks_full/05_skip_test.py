import sys
import pytest


@pytest.mark.skip(reason="This feature is not implemented yet")
def test_skip_function():
    assert False


@pytest.mark.skipif(sys.version_info < (3, 10), reason="This test requires Python 3.10 or less")
def test_skip_function_skipif():
    assert True

@pytest.mark.skipif(sys.platform == "win32", reason="This test is not supported on Windows")
def test_skip_function_skipif_platform():
    assert False

@pytest.mark.xfail(reason="This test is expected to fail")
def test_xfail_function():
    assert 10/0

