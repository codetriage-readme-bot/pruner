# Pruner
Pruner is your best friend when it comes to pruning your Python requirements file.
Pruner will run over your requirements and test each one against your test command.
If your projects test command fails then we know the package needs to remain in the requirements
otherwise we prune it.

# Installation
```
pip install pruner
```

# Usage

```
usage: pruner.py [-h]
                 requirements_file output_file
                 [test_command [test_command ...]]
```


# Example
```
> pruner requirements.txt pruned_requirements.txt python myproj.py

PRUNER: virtualenv prunertests
PRUNER: source prunertests/bin/activate
PRUNER: pip install -r requirements.txt
PRUNER: Running initial test...
PRUNER: Initial test was a success, beginning requirement tests...
PRUNER: Testing django
PRUNER: django was needed
PRUNER: Testing delegator
PRUNER: delegator was not needed
PRUNER: Testing rancat
PRUNER: rancat was needed
PRUNER: Testing flask
PRUNER: flask was not needed
PRUNER: Testing crayons
PRUNER: crayons was not needed
PRUNER: Testing requests
PRUNER: requests was not needed
PRUNER: deactivate
PRUNER: rm -rf prunertests
PRUNER: Writing results to pruned_requirements.txt
PRUNER: DONE

> cat requirements.txt
garbagepackage3
rancat
django
garbagepackage1
garbagepackage2

> cat pruned_requirements.txt
django
rancat

> cat myproj.py
import argparse
import sys
import django
import rancat
```
