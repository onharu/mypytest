def greeting(name: str) -> str:
    return 'Hello ' + name

greeting(3)         # Argument 1 to "greeting" has incompatible type "int"; expected "str"
#greeting(b'Alice')  # Argument 1 to "greeting" has incompatible type "bytes"; expected "str"
greeting("World!")  # No error