# LaunchPy

LaunchPy is made to reduce your time setting up many environments.

## How To Use

### From Source

1. Clone the repo
2. Create a launchpy.yml file with instructions (use the Example below as a starting point)
3. Run `python main.py name` (replace name with the environment you want to start.)

### From Pip

Soon

## Example

```yml
company:
  react:
    path: path/to/react-project
    commands:
      - yarn start

  python-backend:
    path: path/to/python-project
    virtualenv: venv
    commands:
      - uvicorn --reload

  node-microservice:
    path: path/to/node-project
    commands:
      - node micro.js
```

With the example above `python main.py company` would start all the processes: React, Python-Backend and Node-Microservice
