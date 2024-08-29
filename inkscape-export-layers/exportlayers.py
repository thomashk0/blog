#!/usr/bin/env python3

"""
Export a subset of layers from a SVG file.
"""

from xml.dom import minidom
import argparse
import subprocess
import tempfile
import os

INKSCAPE_SUPPORTED_EXTENSIONS = [".pdf", ".ps", ".eps", ".png"]
EXPORT_LAYERS_VERSION = (1, 0, 0)


class InkscapeUnsupportedExtention(Exception):
    pass


def inkscape_export(src, dst, user_args=[]):
    """ Calls inkscape externally to export a SVG file into another format

        :raises InkscapeUnsupportedExtention:
            if the output format is unsupported
    """
    _, ext = os.path.splitext(dst)
    if ext not in INKSCAPE_SUPPORTED_EXTENSIONS:
        raise InkscapeUnsupportedExtention

    extra_flags = user_args
    subprocess.check_call(
        ["inkscape", "-o", dst] + extra_flags + [src])


def hide_layers(src, hide, verbose=False):
    """ Hides a set of layers in the file `src` and returns the resulting raw XML
    content

    This is achieved through a (very) naive XML processing.

    :params str src:  path of the input SVG file.
    :params list hide:  a list of layers to hide.
        Each element MUST be a valid layer name in the input file
    :returns bytes: raw XML content

    """
    svg = minidom.parse(open(src, mode='r'))
    g_hide = []
    g_show = []

    for g in svg.getElementsByTagName("g"):
        group_mode = g.attributes.get("inkscape:groupmode")
        if group_mode is None:
            continue
        if group_mode.value == "layer" and "inkscape:label" in g.attributes:
            label = g.attributes["inkscape:label"].value
            if label in hide:
                g.attributes['style'] = 'display:none'
                g_hide.append(g)
            else:
                g.attributes['style'] = 'display:inline'
                g_show.append(g)
    if verbose:
        print("hiding {:d}/{:d} nodes".format(len(g_hide),
                                              len(g_hide + g_show)))
    return svg.toxml()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--hide', metavar='layer-name', action='append', default=[],
        help=(
            "comma separated list of additional layers to hide, "
            "can be specified multiple times"))
    parser.add_argument('-i', '--inkscape-args', action='append', default=[],
                        help="extra arguments to be passed to Inkscape export")
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="display debug messages")
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help="show current version and exit")
    parser.add_argument(
        '-o', '--output',
        metavar='OUTPUT',
        help=(
            "path to the output file (supported extensions : " +
            ", ".join(INKSCAPE_SUPPORTED_EXTENSIONS) +
            ")"))
    parser.add_argument('src', metavar='INPUT', nargs='?',
                        default=None,
                        help='input SVG file')
    args = parser.parse_args()

    if args.version:
        major, minor, patch = EXPORT_LAYERS_VERSION
        print("exportlayers {:d}.{:d}.{:d}".format(major, minor, patch))
        return

    if not args.src:
        parser.error("no input file specified")

    with tempfile.NamedTemporaryFile(mode='wb', suffix='.svg') as tmp:
        hide_list = [x.strip() for h in args.hide for x in h.split(',')]
        res_xml = hide_layers(args.src, hide_list, verbose=args.verbose)
        tmp.write(res_xml.encode('utf-8'))

        try:
            inkscape_export(tmp.name, args.output,
                            user_args=args.inkscape_args)
        except InkscapeUnsupportedExtention:
            parser.error(
                "Unsupported Inkscape export format for file " + args.output)


if __name__ == '__main__':
    main()
