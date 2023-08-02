# Project Zero

A demonstration of a (relatively) complete
solution with test cases, and documentation.

## Installation

This isn't installed with PIP. Instead,
checkout the Github repository.

After checkout, use the ``requirements-dev.txt``
to install the needed development components.

```bash
python -m pip install -r requirements-dev.txt
```

The documentation uses PlantUML.
See https://pypi.org/project/sphinxcontrib-plantuml/
and https://plantuml.com/running for more information.

## Demonstration

To run the application, using the following command:

```bash
python src/hello_world.py
```

## Testing

To show that it works, run the `tox` command.

```bash
tox
```

## Documentation

To rebuild the documentation use Sphinx.

```bash
cd docs
make html
```

## Building an Initial Python Environment

One way to get started is to use Conda to build the environment.
Conda can be downloaded via the Miniconda installer.
See https://docs.conda.io/en/latest/miniconda.html

Then the following conda commands will populate enough
Python (and tools) to build an environment

```bash
conda create -n projectbook --channel=conda-forge python=3.11
conda activate projectbook
conda install --channel=conda-forge pip-tools
```

When the conda environment is active, the name will be
at the start of the prompt.
It might look like this:

```
(projectbook) %
```

It might be more involved, depending on how much information is included
in your prompt.

With the `pip-compile` command, the list of required packages
in the `pyproject.toml` can be turned into a complete list
of packages to install.

```bash
pip-compile --all-extras -o requirements-dev.txt
pip install -r requirements-dev.txt
```


