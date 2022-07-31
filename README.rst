.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/k8s_builder.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/k8s_builder
    .. image:: https://readthedocs.org/projects/k8s_builder/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://k8s_builder.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/k8s_builder/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/k8s_builder
    .. image:: https://img.shields.io/pypi/v/k8s_builder.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/k8s_builder/
    .. image:: https://img.shields.io/conda/vn/conda-forge/k8s_builder.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/k8s_builder
    .. image:: https://pepy.tech/badge/k8s_builder/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/k8s_builder
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/k8s_builder

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===========
k8s_builder
===========


    Builds and maintains the base k8s components for builders


A longer description of your project goes here...


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

===
Dev
===

sudo apt install python3-pip
sudo apt install python3 python3-venv python3-pip
sudo python3 -m pip install -U pyscaffold[all]
sudo python3 -m pip install virtualenv
git config --global user.email "30276587+gazzasaur@users.noreply.github.com"
git config --global user.name "gazzasaur"
putup -i k8s_builder

cd k8s_builder/
. .venv/bin/activate
tox -e build
python3 -m pip install -e .
tox

# If tests fail due to dependencies recreate everything
tox -r
