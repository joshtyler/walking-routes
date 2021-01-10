GPX_SRC_DIR=$(abspath ../data/gpx)
TOML_SRC_DIR=$(abspath ../data/walks)
RAW_KML_OUT_DIR=$(abspath ../gen/kml)
PROCESSED_KML_OUT_DIR=$(abspath ../gen/walks)

TOML_SRC_FILES=$(wildcard $(TOML_SRC_DIR)/*.toml)
GPX_SRC_FILES=$(wildcard $(GPX_SRC_DIR)/*.gpx)
RAW_KML_OUT_FILES=$(patsubst $(GPX_SRC_DIR)/%.gpx,$(RAW_KML_OUT_DIR)/%.kml,$(GPX_SRC_FILES))
PROCESSED_KML_OUT_FILES=$(patsubst $(TOML_SRC_DIR)/%.toml,$(PROCESSED_KML_OUT_DIR)/%.kml,$(TOML_SRC_FILES))

.PHONY: proc_kml
all: proc_kml
proc_kml: $(PROCESSED_KML_OUT_FILES)
	@echo $(PROCESSED_KML_OUT_FILES)

.PHONY: raw_kml
raw_kml : $(RAW_KML_OUT_FILES)

$(RAW_KML_OUT_DIR)/%.kml : $(GPX_SRC_DIR)/%.gpx
	mkdir -p $(RAW_KML_OUT_DIR)
	./gpxtokml.sh $^ > $@

$(PROCESSED_KML_OUT_DIR)/%.kml : $(TOML_SRC_DIR)/%.toml raw_kml
	mkdir -p $(PROCESSED_KML_OUT_DIR)
	./processconfig.py $< > $@

.PHONY: clean
clean:
	rm -rf $(RAW_KML_OUT_DIR)
	rm -rf $(PROCESSED_KML_OUT_DIR)
