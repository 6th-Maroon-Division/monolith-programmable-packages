# Contributing

## Required PR metadata
- Exactly one label: patch, minor, or major
- PR body must include a :cl: changelog block

## Package version folder
Each package version must contain:
- lib.lua
- dependencies.txt
- meta.yml

Path format:
packages/<name>/<version>/

## meta.yml required keys
- name
- version
- minAbi
- maxAbi
- changelog

Optional:
- checksum
- requires_same_as

## Dependency inheritance
If dependencies are unchanged from another version, use:
requires_same_as: <version>

## Changelog entry types
Allowed types:
- add
- fix
- tweak
- remove

Example:
:cl:
- add: Added package resolver cache
- fix: Fixed invalid version parsing
