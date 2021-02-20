# Pymesh Smart Contracts in Python

[![Build Status](https://travis-ci.com/pymesh/Pymesh.svg?branch=master)](https://travis-ci.com/pymesh/Pymesh)
[![PyPI version](https://badge.fury.io/py/Pymesh.svg)](https://badge.fury.io/py/Pymesh)
[![Documentation Status](https://readthedocs.org/projects/Pymesh/badge/?version=latest)](https://Pymesh.readthedocs.io/en/latest/?badge=latest)

Pymesh is a Python language binding for [pymesh Smart Contracts (ASC1s)](https://developer.pymesh.org/docs/asc). 

pymesh Smart Contracts are implemented using a new language that is stack-based, 
called [Transaction Execution Approval Language (TEAL)](https://developer.pymesh.org/docs/teal). 
This a non-Turing complete language that allows branch forwards but prevents recursive logic 
to maximize safety and performance. 

However, TEAL is essentially an assembly language. With Pymesh, developers can express smart contract logic purely using Python. 
Pymesh provides high level, functional programming style abstactions over TEAL and does type checking at construction time.

Pymesh **hasn't been security audited**. Use it at your own risk.

### Install 

Pymesh requires python version >= 3.6

* `pip3 install Pymesh`

### Documentation

[Pymesh Docs](https://Pymesh.readthedocs.io/)

### Run Demo

In Pymesh root directory:

* `jupyter notebook demo/Pymesh\ Demonstration.ipynb`


### Development Setup

Setup venv (one time):
 * `python3 -m venv venv`


Active venv:
 * `. venv/bin/activate.fish` (if your shell is fish)
 * `. venv/bin/activate` (if your shell is bash/zsh)


Pip install Pymesh in editable state
 * `pip install -e .`
 
Type checking using mypy
* `mypy Pymesh`

Run tests:
* `pytest`
