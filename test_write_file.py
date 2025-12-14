from functions.write_files import write_file


def run_test():
    # 1) Write to existing file in working directory
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print('Result for writing to "lorem.txt":')
    print(result)
    print()
    # "wait, this isn't lorem ipsum" → 28 characters
    assert result == 'Successfully wrote to "lorem.txt" (28 characters written)'

    # 2) Write to a new file inside a subdirectory of working directory
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print('Result for writing to "pkg/morelorem.txt":')
    print(result)
    print()
    # "lorem ipsum dolor sit amet" → 26 characters
    assert result == 'Successfully wrote to "pkg/morelorem.txt" (26 characters written)'

    # 3) Attempt to write outside the working directory (should be blocked)
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print('Result for writing to "/tmp/temp.txt":')
    print(result)
    print()
    assert result == 'Error: Cannot list /tmp/temp.txt as it is outside the permitted working directory'


if __name__ == "__main__":
    run_test()