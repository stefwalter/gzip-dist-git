# Makefile for source rpm: gzip
# $Id$
NAME := gzip
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
