from docutils import nodes
from docutils.statemachine import ViewList
from docutils.parsers.rst import Directive
import subprocess
import sphinx
from sphinx.util.nodes import nested_parse_with_titles
import os.path


class EmbedN2Directive(Directive):
    """
    EmbedN2Directive is a custom directive to build and embed an N2 diagram into docs
    An example usage would look like this:

    .. embed-n2::
        ../../examples/model.py

    The 1 argument is the model file to be diagrammed.

    What the above will do is replace the directive and its arg with an N2 diagram.

    """

    required_arguments = 1
    optional_arguments = 0
    has_content = True

    def run(self):
        path_to_model = self.arguments[0]

        np = os.path.normpath(os.path.join(os.getcwd(), path_to_model))

        # check that the file exists
        if not os.path.isfile(np):
            raise IOError('File does not exist({0})'.format(np))

        html_name = os.path.join(os.getcwd(), (os.path.basename(path_to_model).split('.')[0] + "_n2.html"))

        subprocess.Popen(['openmdao', 'view_model', np, '--no_browser', '--embed', '-o' + html_name])

        # add raw embed for HTML file
        doc_nodes = []

        source = "\n.. raw:: html\n"
        source += "   :file: " + html_name + "\n"

        body = nodes.literal_block(source, source)
        # body['language'] = 'html'

        # body.append(".. raw:: html")
        # body.append("   :file: %s" % html_name)

        doc_nodes.append(body)

        return doc_nodes


def setup(app):
    """add custom directive into Sphinx so that it is found during document parsing"""
    app.add_directive('embed-n2', EmbedN2Directive)

    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
