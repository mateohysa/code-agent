from functions.get_file_content import get_file_content
from config import MAX_FILE_CONTENT_LENGTH


def run_test():
    # Test truncation behavior for a large file
    trunc_msg = f'[...File "lorem.txt" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
    result = get_file_content("calculator", "lorem.txt")

    print('Result for "lorem.txt" (truncation test):')
    print(f"Total length: {len(result)}")
    print(f"Ends with truncation message: {result.endswith(trunc_msg)}")

    # The file is larger than MAX_FILE_CONTENT_LENGTH, so the returned
    # content should be exactly the truncated length plus the suffix.
    assert len(result) == MAX_FILE_CONTENT_LENGTH + len(trunc_msg)
    assert result.endswith(trunc_msg)

    print()

    # Additional test cases, printing outputs
    paths = [
        "main.py",
        "pkg/calculator.py",
        "/bin/cat",
        "pkg/does_not_exist.py",
    ]

    for p in paths:
        output = get_file_content("calculator", p)
        print(f'Result for "{p}":')
        print(output)
        print()


if __name__ == "__main__":
    run_test()
