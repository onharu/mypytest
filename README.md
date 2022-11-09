# Using mypy to get the typed Python AST(wip)

## Step 1: Install the latest mypy

Install the latest (github master) mypy (which fixes [this issue](https://github.com/python/mypy/pull/10125)):

```sh
python3 -m pip install -U git+https://github.com/python/mypy.git
```

Output:
```
Successfully installed mypy-1.0.0+dev.dbcbb3f5c3ef791c98088da0bd1dfa6cbf51f301
```

## Step 2: Run the example

The example [mypytest.py](mypytest.py) traverses the AST of the following code ([ex1.py](ex1.py)) using `NodeVisitor`, and outputs the type of the return value `builtins.int`.

### The code to be analyzed:
```python
def f(x:int):
    return x + 1
```

### Command line:
```sh
rm -rf .mypy_cache; python3 mypytest.py
```

(We need to remove the entire cache folder to get the whole AST.)

### Output:
```
LOG:  Could not load plugins snapshot: @plugins_snapshot.json

LOG:  Mypy Version:           1.0.0+dev.dbcbb3f5c3ef791c98088da0bd1dfa6cbf51f301
LOG:  Config File:            Default
LOG:  Configured Executable:  /usr/local/opt/python@3.10/bin/python3.10
LOG:  Current Executable:     /usr/local/opt/python@3.10/bin/python3.10
LOG:  Cache Dir:              .mypy_cache
LOG:  Compiled:               False

...

OG:  Processing SCC singleton (ex1) as inherently stale with stale deps (builtins)
LOG:  Writing ex1 ex1.py ex1.meta.json ex1.data.json
LOG:  Cached module ex1 has changed interface
LOG:  No fresh SCCs left in queue
LOG:  Build finished in 3.973 seconds with 44 modules, and 0 errors
Success: no issues found in 1 source file
init success
visit block
visit return stmt
builtins.int
```

`builtins.int` in the last line says that the inferred type for `x + 1` is the primitive `int` type.

