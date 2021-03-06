"""Tests for contextual menu building

These integration tests guarantee that the compiler plugin is emitting the
right stuff and that that stuff makes it through the DXR clang plugin
unscathed.

"""
from nose import SkipTest

from dxr.testing import DxrInstanceTestCase, menu_on


class MenuTests(DxrInstanceTestCase):
    """Generally, the tests herein make sure the definition of the referenced
    thing is found (for refs) and that the qualname is extracted properly (by
    testing a representative search menuitem).

    """
    def test_includes(self):
        """Make sure #include cross references are linked."""
        menu_on(self.source_page('main.cpp'),
                '"extern.c"',
                {'html': 'Jump to file',
                 'href': '/code/source/extern.c'})

    def test_functions(self):
        """Make sure functions are found and have a representative sane menu item."""
        menu_on(self.source_page('extern.c'),
                'another_file',
                {'html': 'Find declarations',
                 'href': '/code/search?q=%2Bfunction-decl%3Aanother_file%28%29'})

    def test_function_refs(self):
        """Make sure definitions are found and a representative qualname-using
        search is properly constructed."""
        menu_on(self.source_page('main.cpp'),
                'another_file',
                {'html': 'Jump to definition',
                 'href': '/code/source/extern.c#7'},
                {'html': 'Find callers',
                 'href': '/code/search?q=%2Bcallers%3Aanother_file%28%29'})

    def test_variables(self):
        """Make sure var declarations are found and have a representative sane
        menu item."""
        menu_on(self.source_page('main.cpp'),
                'var',
                {'html': 'Find references',
                 'href': '/code/search?q=%2Bvar-ref%3Avar'})

    def test_variable_refs(self):
        """Make sure definitions are found and a representative qualname-using
        search is properly constructed."""
        menu_on(self.source_page('main.cpp'),
                'var',
                {'html': 'Jump to definition',
                 'href': '/code/source/extern.c#11'},
                {'html': 'Find declarations',
                 'href': '/code/search?q=%2Bvar-decl%3Avar'})

    def test_type(self):
        menu_on(self.source_page('extern.c'),
                'numba',
                {'html': 'Find references',
                 'href': '/code/search?q=%2Btype-ref%3Anumba'})

    def test_type_ref(self):
        menu_on(self.source_page('main.cpp'),
                'MyClass',
                {'html': 'Jump to definition',
                 'href': '/code/source/extern.c#14'},
                {'html': 'Find declarations',
                 'href': '/code/search?q=%2Btype-decl%3AMyClass'})

    def test_decldef(self):
        """Make sure prototypes, declarations, and such get menus."""
        menu_on(self.source_page('extern.c'),
                'MyClass',
                {'html': 'Find references',
                 'href': '/code/search?q=%2Btype-ref%3AMyClass'})

    def test_typedef(self):
        menu_on(self.source_page('extern.c'),
                'numba',
                {'html': 'Find references',
                 'href': '/code/search?q=%2Btype-ref%3Anumba'})

    def test_typedef_ref(self):
        menu_on(self.source_page('main.cpp'),
                'numba',
                {'html': 'Jump to definition',
                 'href': '/code/source/extern.c#5'},
                {'html': 'Find references',
                 'href': '/code/search?q=%2Btype-ref%3Anumba'})

    def test_namespace(self):
        menu_on(self.source_page('extern.c'),
                'Space',
                {'html': 'Find definitions',
                 'href': '/code/search?q=%2Bnamespace%3ASpace'})

    def test_namespace_ref(self):
        menu_on(self.source_page('main.cpp'),
                'Space',
                {'html': 'Jump to definition',
                 'href': '/code/source/extern.c#18'},
                {'html': 'Find references',
                 'href': '/code/search?q=%2Bnamespace-ref%3ASpace'})

    def test_namespace_alias(self):
        menu_on(self.source_page('extern.c'),
                'Bar',
                {'html': 'Find references',
                 'href': '/code/search?q=%2Bnamespace-alias-ref%3ABar'})

    def test_namespace_alias_ref(self):
        menu_on(self.source_page('main.cpp'),
                'Bar',
                {'html': 'Jump to definition',
                 'href': '/code/source/extern.c#21'},
                {'html': 'Find references',
                 'href': '/code/search?q=%2Bnamespace-alias-ref%3ABar'})

    def test_macro(self):
        menu_on(self.source_page('extern.c'),
                'MACRO',
                {'html': 'Find references',
                 'href': '/code/search?q=%2Bmacro-ref%3AMACRO'})

    def test_macro_ref(self):
        menu_on(self.source_page('main.cpp'),
                'MACRO',
                {'html': 'Jump to definition',
                 'href': '/code/source/extern.c#23'},
                {'html': 'Find references',
                 'href': '/code/search?q=%2Bmacro-ref%3AMACRO'})

    def test_deep_files(self):
        """Make sure we process files not at the root level."""
        menu_on(self.source_page('deeper_folder/deeper.c'),
                'deep_thing',
                {'html': 'Find references',
                 'href': '/code/search?q=%2Btype-ref%3Adeep_thing'})
