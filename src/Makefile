
# Inputs
GPX_SRC_DIR=$(abspath ../data/gpx)
TOML_SRC_DIR=$(abspath ../data/walks)

# Cached files (update_cached rule populates these folders based on toml contents)
CACHED_GPX_DIR=$(abspath ../cache/gpx)

# update_cached_gpx will iterate toml files looking for remote GPX files
# If we have them already cached, it will leave them
# If we don't have them, it will download them
# It wil print out all the cached filenames, downloaded or not
# We can't have this as a rule because the other variables need the list of input files(!)
CACHED_GPX_FILES=$(shell mkdir -p $(CACHED_GPX_DIR) && ./update_cached_gpx.py $(CACHED_GPX_DIR) firefox_osmaps_curl_cmd.txt $(TOML_SRC_FILES))

# Generated files (intermediate and output)
GENERATED_DIR=$(abspath ../gen)
INTERMEDIATE_KML_DIR=$(abspath $(GENERATED_DIR)/kml)
MERGED_GPX_DIR=$(abspath $(GENERATED_DIR)/mergedgpx)

# Genrate one final output KML per toml input
TOML_SRC_FILES=$(wildcard $(TOML_SRC_DIR)/*.toml)
PROCESSED_KML_OUT_FILES=$(patsubst $(TOML_SRC_DIR)/%.toml,$(GENERATED_DIR)/%.kml,$(TOML_SRC_FILES))

# We get gpx source files both from the source and from the cache
GPX_SRC_FILES+=$(notdir $(wildcard $(GPX_SRC_DIR)/*.gpx))
GPX_SRC_FILES+=$(notdir $(CACHED_GPX_FILES))
#Generate an intermediate KML per source GPX
INTERMEDIATE_KML_FILES=$(addsuffix .kml, $(addprefix $(INTERMEDIATE_KML_DIR)/, $(basename $(GPX_SRC_FILES))))

.PHONY: all
all: $(PROCESSED_KML_OUT_FILES)
proc_kml: $(PROCESSED_KML_OUT_FILES)

.PHONY: print
print:
	@echo $(INTERMEDIATE_KML_FILES)
	@echo $(CACHED_GPX_FILES)

# Stage all the GPX files in one directory to make life easier
$(MERGED_GPX_DIR)/%.gpx: $(CACHED_GPX_DIR)/%.gpx
	mkdir -p $(MERGED_GPX_DIR)
	cp $^  $(MERGED_GPX_DIR)/

$(MERGED_GPX_DIR)/%.gpx: $(GPX_SRC_DIR)/%.gpx
	mkdir -p $(MERGED_GPX_DIR)
	cp $^  $(MERGED_GPX_DIR)/

# Process each GPX file into its own KML
$(INTERMEDIATE_KML_DIR)/%.kml : $(MERGED_GPX_DIR)/%.gpx
	mkdir -p $(INTERMEDIATE_KML_DIR)
	./gpxtokml.sh $^ > $@

# For each TOML file create a merged KML file based on the TOML contents
# We have all the GPX files available
$(GENERATED_DIR)/%.kml : $(TOML_SRC_DIR)/%.toml $(INTERMEDIATE_KML_FILES)
	./processconfig.py $< > $@

.PHONY: clean clean_cached
clean:
	rm -rf $(GENERATED_DIR)

# Depend on clean so that clean_cached becomes "superclean"
clean_cached: clean
	rm -r $(CACHED_GPX_DIR)
