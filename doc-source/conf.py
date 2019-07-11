#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('./demo/'))

from sphinx.locale import _

import os
import shutil
if os.path.exists("../wx"):
    shutil.rmtree("../wx")

os.mkdir("../wx")

with open("../wx/__init__.py", "w") as f:
    f.write("""
def dummy_function(*args, **kwargs):
	return 0


App = object
FD_SAVE = 0
FD_OVERWRITE_PROMPT = 0
ID_ANY = 0
DefaultPosition = 0
DefaultSize = 0
TAB_TRAVERSAL = 0
Panel = object
Dialog = object
Frame = object

PlatformInfo = []

PyEventBinder = NewEventType = FileDialog = Bitmap = NewIdRef = dummy_function

Button = object

DEFAULT_FRAME_STYLE = 0
CLIP_CHILDREN = 0
SUNKEN_BORDER = 0
ID_CANCEL = 0
FONTWEIGHT_LIGHT = 0
FONTWEIGHT_NORMAL = 0
FONTWEIGHT_BOLD = 0
FONTSTYLE_ITALIC = 0
FONTSTYLE_NORMAL = 0
FONTSTYLE_SLANT = 0
FONTFAMILY_SWISS = 0
FONTFAMILY_ROMAN = 0
FONTFAMILY_SCRIPT = 0
FONTFAMILY_DECORATIVE = 0
FONTFAMILY_MODERN = 0
CAP_BUTT = 0
CAP_PROJECTING = 0
CAP_ROUND = 0
JOIN_BEVEL = 0
JOIN_MITER = 0
JOIN_ROUND = 0

WXK_PAGEUP = 0
WXK_PAGEDOWN = 0
WXK_CONTROL = 0
WXK_SHIFT = 0
WXK_ALT = 0
WXK_LEFT = 0
WXK_UP = 0
WXK_RIGHT = 0
WXK_DOWN = 0
WXK_ESCAPE = 0
WXK_F1 = 0
WXK_F2 = 0
WXK_F3 = 0
WXK_F4 = 0
WXK_F5 = 0
WXK_F6 = 0
WXK_F7 = 0
WXK_F8 = 0
WXK_F9 = 0
WXK_F10 = 0
WXK_F11 = 0
WXK_F12 = 0
WXK_SCROLL = 0
WXK_PAUSE = 0
WXK_BACK = 0
WXK_RETURN = 0
WXK_INSERT = 0
WXK_DELETE = 0
WXK_HOME = 0
WXK_END = 0
WXK_PAGEUP = 0
WXK_PAGEDOWN = 0
WXK_NUMPAD0 = 0
WXK_NUMPAD1 = 0
WXK_NUMPAD2 = 0
WXK_NUMPAD3 = 0
WXK_NUMPAD4 = 0
WXK_NUMPAD5 = 0
WXK_NUMPAD6 = 0
WXK_NUMPAD7 = 0
WXK_NUMPAD8 = 0
WXK_NUMPAD9 = 0
WXK_NUMPAD_ADD = 0
WXK_NUMPAD_SUBTRACT = 0
WXK_NUMPAD_MULTIPLY = 0
WXK_NUMPAD_DIVIDE = 0
WXK_NUMPAD_DECIMAL = 0
WXK_NUMPAD_ENTER = 0
WXK_NUMPAD_UP = 0
WXK_NUMPAD_RIGHT = 0
WXK_NUMPAD_DOWN = 0
WXK_NUMPAD_LEFT = 0
WXK_NUMPAD_PAGEUP = 0
WXK_NUMPAD_PAGEDOWN = 0
WXK_NUMPAD_HOME = 0
WXK_NUMPAD_END = 0
WXK_NUMPAD_INSERT = 0
WXK_NUMPAD_DELETE = 0

CURSOR_HAND = 0
CURSOR_ARROW = 0
CURSOR_CROSS = 0
CURSOR_WAIT = 0

ToolBar = object
StatusBar = object
Printout = object
TB_HORIZONTAL = 0

    """)

with open("../wx/stc.py", "w") as f:
    f.write("""
StyledTextCtrl = object
    """)


project = "domdf_wxpython_tools"
from domdf_wxpython_tools import __author__, __version__, __copyright__


slug = re.sub(r'\W+', '-', project.lower())
version = __version__
release = __version__
author = __author__
copyright = __copyright__
language = 'en'

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinxcontrib.httpdomain',
]

templates_path = ['_templates']
source_suffix = '.rst'
exclude_patterns = []

master_doc = 'index'
suppress_warnings = ['image.nonlocal_uri']
pygments_style = 'default'

intersphinx_mapping = { # Is this where those mystery links are specified?
    'rtd': ('https://docs.readthedocs.io/en/latest/', None),
    'sphinx': ('http://www.sphinx-doc.org/en/stable/', None),
}

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,  # True will show just the logo
}
html_theme_path = ["../.."]
#html_logo = "logo/pyms.png"
html_show_sourcelink = False    # True will show link to source

html_context = {
    # Github Settings
    "display_github": True, # Integrate GitHub
    "github_user": "domdfcoding", # Username
    "github_repo": "domdf_wxpython_tools", # Repo name
    "github_version": "master", # Version
    "conf_py_path": "/", # Path in the checkout to the docs root
}

htmlhelp_basename = slug

latex_documents = [
  ('index', '{0}.tex'.format(slug), project, author, 'manual'),
]

man_pages = [
    ('index', slug, project, [author], 1)
]

texinfo_documents = [
  ('index', slug, project, author, slug, project, 'Miscellaneous'),
]


# Extensions to theme docs
def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field

    app.add_object_type(
        'confval',
        'confval',
        objname='configuration value',
        indextemplate='pair: %s; configuration value',
        doc_field_types=[
            PyField(
                'type',
                label=_('Type'),
                has_arg=False,
                names=('type',),
                bodyrolename='class'
            ),
            Field(
                'default',
                label=_('Default'),
                has_arg=False,
                names=('default',),
            ),
        ]
    )
