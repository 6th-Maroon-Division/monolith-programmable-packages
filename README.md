# monolith-programmable-packages

Monolith programmable computer packages, BIOS releases, and package index.

## Purpose
This repository is the canonical source for programmable computer Lua packages and BIOS artifacts.

## Layout
- packages/<package-name>/<version>/lib.lua
- packages/<package-name>/<version>/dependencies.txt
- packages/<package-name>/<version>/meta.yml
- index/index.json

## ABI Compatibility
Each package version declares:
- minAbi
- maxAbi

A runtime with ABI N may install a package version only if:
minAbi <= N <= maxAbi

## Versioning
Semantic versioning is used:
major.minor.patch

PR label determines bump type:
- major
- minor
- patch

## Changelog in PR Body
Use this format:

:cl:
- add: Added feature
- fix: Fixed bug
- tweak: Behavior change
- remove: Removed feature

## Local Development
1. Add or update package version folders under packages.
2. Ensure required files exist.
3. Open PR with one bump label and a :cl: block.
4. CI validates and rebuilds index.

## Example meta.yml
name: bios-core
version: 1.0.0
minAbi: 1
maxAbi: 1
checksum: ""
changelog:
  - type: add
    message: Initial BIOS release
