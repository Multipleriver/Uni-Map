#!/bin/bash

trap 'find . -type d -name "__pycache__" -exec rm -rf {} +' EXIT
flask run
