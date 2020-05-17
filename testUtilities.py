def assertThrows(function, expectedException):
    error = None
    try:
        function()
    except Exception as e:
        error = e
    assert isinstance(error, expectedException)


def assertDoesntThrow(function):
    error = None
    try:
        function()
    except Exception as e:
        error = e
    assert error is None
