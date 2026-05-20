#!/bin/bash
rm -rf dist/ build/ *.egg-info
python3.9 -m build
twine upload dist/*
