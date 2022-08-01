===========
k8s_builder
===========


    Builds and maintains the base k8s components for builders

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

===
Dev
===

Getting Started
===============

Setting up your environment::
    sudo apt install python3-pip python3-virtualenv

Down the and setup the package::
    git clone
    cd k8s_builder
    virtualenv .venv

Switch to the virtual envinronment::
    . .venv/bin/activate

Install the required packages::
    python3 -m pip install -e .

Build the package::
    tox

If new dependencies are added or after each pull, rebuild the environment::
    tox -r
