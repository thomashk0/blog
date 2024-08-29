# Inkscape Layer Exporter

This simple Python script allows you to select layers to export from a
SVG file. It can be used to produce basic animations in beamer
presentations.

## Basic Usage

By default all layers are shown, you can hide a subset like this:

``` bash
$ ./exportlayers --hide <layername1>,<layername2> <SVG_FILE> <OUTPUT_FILE>
```

The output file extension is matched and `inkscape` is called to export
only the drawing area.

Some example are given in the [Makefile](./Makefile). Run them with
`make` in the current directory.

**Note**: the script `exportlayers.py` does not have more than 100 lines, it is
worth reading it.

## Contributions

Contributions are welcome, feel free to share your improvements !
