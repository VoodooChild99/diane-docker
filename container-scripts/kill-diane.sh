#!/bin/bash

kill -9 `ps ax | grep diane | grep -v grep | grep -v sh | awk '{print $1}'`