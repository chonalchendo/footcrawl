docker := require("docker")
rm := require("rm")
uv := require("uv")


PACKAGE := "footcrawl"
REPOSITORY := "footcrawl"
SOURCES := "src"
TESTS := "tests"

default:
  @just --list

import "tasks/check.just"
import "tasks/format.just"

