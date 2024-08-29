# This makefile shows how you can use the export layer script to generate
# figures

# Add the -D flag to export only the draw area
EXPORT_LAYERS := ./exportlayers.py -i"-D"

ALL_TARGETS := \
	example_layer_background.pdf\
	example_layer_background_bis.pdf\
	example_layer_1.pdf\
	example_all.pdf

all: $(ALL_TARGETS)

.PHONY: clean
clean:
	-rm $(ALL_TARGETS)

# Hide layer_1 and layer_2
example_layer_background.pdf: example/example.svg
	$(EXPORT_LAYERS) --hide=layer_1 --hide=layer_2 -o $@ $<

# Hide layer_1 and layer_2, comma separated flavour
example_layer_background_bis.pdf: example/example.svg
	$(EXPORT_LAYERS) --hide=layer_1,layer_2 -o $@ $<

# Hide layer_2
example_layer_1.pdf: example/example.svg
	$(EXPORT_LAYERS) --hide=layer_2 --output $@ $<

example_all.pdf: example/example.svg
	$(EXPORT_LAYERS) -o $@ $<
