# Graph-tool Extras

Collection of functions and extra algorithms that are not available in [`graph-tool`](https://graph-tool.skewed.de/) but which I have found useful while using the module.

```
src/
 |--- disjoint.py
 |--- suurballe.py
```


## Development
This python environment is manage with [`pipenv`](https://pipenv.pypa.io/en/latest/)
To install all the dependencies in a new python environment, you can run

```bash
pipenv install --dev
```

To run the tests, just type `pytest`

1. To compile the c++ extension and generate the file libdisjoint.so, run `make` in the folder cpp_extension folder
2. 