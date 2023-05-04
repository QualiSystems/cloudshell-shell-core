# CloudShell Shell Core

[![Build status](https://github.com/QualiSystems/cloudshell-shell-core/workflows/CI/badge.svg?branch=master)](https://github.com/QualiSystems/cloudshell-shell-core/actions?query=branch%3Amaster)
[![codecov](https://codecov.io/gh/QualiSystems/cloudshell-shell-core/branch/master/graph/badge.svg)](https://codecov.io/gh/QualiSystems/cloudshell-shell-core)
[![PyPI version](https://badge.fury.io/py/cloudshell-shell-core.svg)](https://badge.fury.io/py/cloudshell-shell-core)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

## Overview

The **cloudshell-shell-core** open source Python package is the base package for all CloudShell shells. It provides basic shell functionality including:
- Resource driver interface, which enables CloudShell to use the shell. This interface is automatically added to the shell’s driver when creating a shell via shellfoundry.
- Definitions of the driver’s context objects, which CloudShell sends to the shell’s commands. For details, see the CloudShell Dev Guide's [Getting information from cloudshell](https://devguide.quali.com/shells/9.3.0/getting-information-from-cloudshell.html)
- [cloudshell-automation-api](https://help.quali.com/Online%20Help/0.0/Python-API/) wrapper. Use of the CloudShell Automation API mostly applies to setting live status and writing messages to output. Other API capabilities are outside the scope of the shell and should be implemented on the sandbox orchestration level,
- [cloudshell-logging](https://github.com/QualiSystems/cloudshell-logging/blob/dev/README.md) wrapper

## Installation
```bash
pip install cloudshell-shell-core
```

**_Python 3 is supported starting with version 5.0.x._**

## Implementation Examples

**Driver’s interface - declaring the driver’s interface for shell 'DataModelExample':**
```python
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
class DataModelExampleDriver (ResourceDriverInterface):
```
#### Api wrapper - returning api session:
```python
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
with CloudShellSessionContext(context) as session:
    perform_validations(session)
    do_some_logic(session)
    do_some_more_logic(session)
```
#### Logging wrapper - how to use the logger:
```python
from cloudshell.shell.core.session.logging_session import LoggingSessionContext 
with LoggingSessionContext(context) as logger:
    do_something(logger)
    do something_else(logger)
```
or
```python
from cloudshell.shell.core.session.logging_session import LoggingSessionContext 
logger = LoggingSessionContext.get_logger_with_thread_id(context)
do_something(logger)
```

#### Driver Context:

The driver context objects are extensively documented in the CloudShell Developer Guide's [Getting Information from CloudShell](https://devguide.quali.com/shells/9.3.0/getting-information-from-cloudshell.html) article. We recommend checking the most up to date version as we periodically update the CloudShell Developer Guide.


We use tox and pre-commit for testing. [Services description](https://github.com/QualiSystems/cloudshell-package-repo-template#description-of-services)
