#!/bin/bash
echo "---Generating python requirements---"
nox -s generate_requirements
echo "---Finished generating python requirements---"

echo "---Generating pants lockfile---"
pants generate-lockfiles
echo "---Finished generating pants lockfile---"
