from functions.run_python_file import run_python_file


def run_test():
    # 1) main.py with no args – should show usage instructions
    result = run_python_file("calculator", "main.py")
    print('Result for running "main.py" with no args:')
    print(result)
    print()
    assert "Calculator App" in result
    assert 'Usage: python main.py "<expression>"' in result

    # 2) main.py with an expression – should run the calculator (JSON output)
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print('Result for running "main.py" with "3 + 5":')
    print(result)
    print()
    assert '"expression": "3 + 5"' in result
    assert '"result": 8' in result

    # 3) tests.py – should run the calculator tests successfully
    result = run_python_file("calculator", "tests.py")
    print('Result for running "tests.py":')
    print(result)
    print()
    # unittest output should contain "OK" on success
    assert "OK" in result

    # 4) Attempt to run a file outside the working directory
    result = run_python_file("calculator", "../main.py")
    print('Result for running "../main.py":')
    print(result)
    print()
    assert result == 'Error: Cannot execute "../main.py" as it is outside the permitted working directory'

    # 5) Nonexistent Python file
    result = run_python_file("calculator", "nonexistent.py")
    print('Result for running "nonexistent.py":')
    print(result)
    print()
    assert result == 'Error: File "nonexistent.py" not found.'

    # 6) Existing but non-Python file
    result = run_python_file("calculator", "lorem.txt")
    print('Result for running "lorem.txt":')
    print(result)
    print()
    assert result == 'Error: "lorem.txt" is not a Python file.'


if __name__ == "__main__":
    run_test()