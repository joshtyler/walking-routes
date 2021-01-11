
# Inputs
PATH_SRC_DIR=$(abspath ../data/path)
TOML_SRC_DIR=$(abspath ../data/meta)

# Cached files (update_cached rule populates these folders based on toml contents)
CACHED_PATH_DIR=$(abspath ../cache/path)

# update_cached_gpx will iterate toml files looking for remote GPX files
# If we have them already cached, it will leave them
# If we don't have them, it will download them
# It wil print out all the cached filenames, downloaded or not
# We can't have this as a rule because the other variables need the list of input files(!)
CACHED_PATH_FILES=$(shell mkdir -p $(CACHED_PATH_DIR) && ./update_cached.py $(CACHED_PATH_DIR) firefox_osmaps_curl_cmd.txt $(TOML_SRC_FILES))

# Generated files (intermediate and output)
GENERATED_DIR=$(abspath ../gen)
INTERMEDIATE_KML_DIR=$(abspath $(GENERATED_DIR)/kml)
MERGED_PATH_DIR=$(abspath $(GENERATED_DIR)/mergedpath)

# Genrate one final output KML per toml input
TOML_SRC_FILES=$(wildcard $(TOML_SRC_DIR)/*.toml)
PROCESSED_KML_OUT_FILES=$(patsubst $(TOML_SRC_DIR)/%.toml,$(GENERATED_DIR)/%.kml,$(TOML_SRC_FILES))

# We get path source files both from the source directory and from the cache
PATH_SRC_FILES+=$(notdir $(wildcard $(PATH_SRC_DIR)/*))
PATH_SRC_FILES+=$(notdir $(CACHED_PATH_FILES))

#Generate an intermediate KML per source GPX
INTERMEDIATE_KML_FILES=$(addsuffix .kml, $(addprefix $(INTERMEDIATE_KML_DIR)/, $(basename $(PATH_SRC_FILES))))

.PHONY: all
all: $(PROCESSED_KML_OUT_FILES)

# Stage all the path files in one directory to make life easier
define copy-to-merged =
mkdir -p $(MERGED_PATH_DIR)
cp $^  $(MERGED_PATH_DIR)/
endef
$(MERGED_PATH_DIR)/%: $(CACHED_PATH_DIR)/%
	$(copy-to-merged)
$(MERGED_PATH_DIR)/%: $(PATH_SRC_DIR)/%
	$(copy-to-merged)

# Process each source file into its own KML
define convert-to-kml =
mkdir -p $(INTERMEDIATE_KML_DIR)
./converttokml.sh $^ > $@
endef
$(INTERMEDIATE_KML_DIR)/%.kml : $(MERGED_PATH_DIR)/%.gpx
	$(convert-to-kml)
$(INTERMEDIATE_KML_DIR)/%.kml : $(MERGED_PATH_DIR)/%.FIT
	$(convert-to-kml)

# For each TOML file create a merged KML file based on the TOML contents
# We have all the GPX files available
$(GENERATED_DIR)/%.kml : $(TOML_SRC_DIR)/%.toml $(INTERMEDIATE_KML_FILES)
	./processconfig.py $< > $@

# Cleanup rules
# Be hesitant to remove cached files, since these come from remote
.PHONY: clean clean_cached
clean:
	rm -rf $(GENERATED_DIR)

# Depend on clean so that clean_cached becomes "superclean"
clean_cached: clean
	rm -r $(CACHED_PATH_DIR)
