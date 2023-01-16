#!/bin/bash

VERSION_FILE=".github/version"
TAG_NAME=$1

echo "$TAG_NAME" > $VERSION_FILE
git tag "$TAG_NAME"
