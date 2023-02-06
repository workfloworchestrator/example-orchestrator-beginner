# example orchestrator (beginner workshop)

Example code for the
[orchestrator-core beginner workshop](https://workfloworchestrator.org/orchestrator-core/workshops/beginner/overview/)
from the [Workflow Orchestrator programme](https://workfloworchestrator.org).

## Do the workshop

This repository contains the code that belongs to the 
[orchestrator-core beginner workshop](https://workfloworchestrator.org/orchestrator-core/workshops/beginner/overview/),
and can be used as an example in case you are stuck during the 
workshop exercises. The 
only files you need to copy are the `docker-compose.yml`, to create and run 
the environment used during the workshop, and the `orchestrator-core-gui.env`
that is needed to correctly configure the GUI. Please follow the workshop for 
further instructions.

## Shortcut to working example orchestrator

When in a hurry, or just curious, the example orchestrator can be started by 
following the instructions below. This example implements the products and 
workflows for a simple user and user group administration.

First clone this repository:

```shell
git clone https://github.com/workfloworchestrator/example-orchestrator-beginner.git
```

Use docker compose to start the environment and initialize the database:

```shell
cd example-orchestrator-beginner
docker compose up
```

Stop docker compose, copy the migrations to add the products and workflows 
to the database, and start the environment again:

```shell
# ^C
cp -av examples/*add_user_and_usergroup* migrations/versions/schema
docker compose up
```

Now point your browser to `http://localhost:3000/` and have a look around. 
You can use the `New Process` button to create subscription on the defined 
products.


## Integration tests

The folder `tests/integration_tests` contains tests that ensure the example orchestrator app works correctly with the latest orchestrator-core version.

These tests are automatically executed in a github workflow whenever a new orchestrator-core release is created.

You can also run them manually:

Environment setup:

1. Start the example orchestrator with `docker compose` as described in the previous section
2. Create a virtual environment
```
python -m venv .venv && source .venv/bin/activate
pip install requests pytest
```
3. Run the tests (**WARNING** this will remove all subscriptions in the local database):
```
pytest tests/integration_tests
```
