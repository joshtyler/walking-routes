.PHONY: all trigs

all : trigs

THIS_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
OUTPUT_DIR=$(THIS_DIR)/jekyll_site/autogen_assets

$(OUTPUT_DIR) :
	mkdir -p $(OUTPUT_DIR)

trigs: $(OUTPUT_DIR)/trigs.json

$(OUTPUT_DIR)/trigs.json : $(THIS_DIR)/trigs/trigs.py $(OUTPUT_DIR) 
	$< $@