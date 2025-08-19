import pytest
import importlib.util
from pathlib import Path

# Load micron/builder.py directly to avoid executing micron/__init__.py
root = Path(__file__).resolve().parents[1]
builder_path = root / "micron" / "builder.py"
colors_path = root / "micron" / "colors.py"

spec_c = importlib.util.spec_from_file_location("micron_colors", str(colors_path))
mod_c = importlib.util.module_from_spec(spec_c)
spec_c.loader.exec_module(mod_c)  # type: ignore
Color = mod_c.Color

# Execute builder.py in a fresh namespace where Color is available to satisfy its
# `from .colors import Color` usage (we provide Color directly).
builder_src = builder_path.read_text()
# remove the relative import line since we provide Color in the namespace
builder_src = builder_src.replace('from .colors import Color', '')
builder_ns = {"Color": Color, "__name__": "micron.builder", "__file__": str(builder_path)}
exec(builder_src, builder_ns)
MicronBuilder = builder_ns["MicronBuilder"]


def test_wrap_and_wrap_color_and_attach_link():
    # _wrap
    assert MicronBuilder._wrap('x', '!') == '`!x`!'

    # _wrap_color with Color enum
    res_enum = MicronBuilder._wrap_color('foo', Color.RED, prefix='F', suffix='f')
    assert res_enum == f'`F{Color.RED.value}foo`f'

    # _wrap_color with raw string
    res_str = MicronBuilder._wrap_color('bar', 'abc', prefix='F', suffix='f')
    assert res_str == '`Fabcbar`f'

    # _attach_address_link with non-empty fragment
    attached = MicronBuilder._attach_address_link('label', 'addr', 'page.mu')
    # inner becomes 'label`' so resulting string follows that exact format
    assert attached == '`[label`addr:/page/page.mu]'

    # _attach_address_link with empty fragment
    attached_empty = MicronBuilder._attach_address_link('', 'addr', 'p')
    assert attached_empty == '`[addr:/page/p]'


def test_text_wrapping_order_and_build():
    b = MicronBuilder()
    # compute expected by applying the same helpers in the same order
    raw = 'hello'
    expected = MicronBuilder._wrap(MicronBuilder._wrap(MicronBuilder._wrap(raw, '!'), '*'), '_')

    b.text('hello', bold=True, italic=True, underline=True)
    assert b.build() == expected


def test_color_and_bgcolor_behavior():
    b = MicronBuilder()
    # color as enum, bgcolor as raw string
    b.text('hi', color=Color.BLUE, bgcolor='123')

    # color applied first, then bgcolor (wrapping the colored fragment)
    nested = MicronBuilder._wrap_color('hi', Color.BLUE, prefix='F', suffix='f')
    expected = MicronBuilder._wrap_color(nested, '123', prefix='B', suffix='b')
    assert b.build() == expected


def test_alignment_and_padding_and_links():
    # center alignment
    b = MicronBuilder()
    b.text('C', center=True)
    assert b.build() == '\n`c\nC\n`a'

    # right alignment
    b = MicronBuilder()
    b.text('R', right=True)
    assert b.build() == '\n`r\nR\n`a'

    # padding 2 adds two newlines before and after
    b = MicronBuilder()
    b.text('P', padding=2)
    assert b.build() == '\n\nP\n\n'

    # address_link with non-empty content attaches as described
    b = MicronBuilder()
    b.text('lbl', address_link='xaddr')
    # because the link is attached before styling/padding, ensure it appears
    assert '`[lbl`xaddr:/page/index.mu]' in b.build()

    # address_link with empty content
    b = MicronBuilder()
    b.text('', address_link='only')
    assert b.build() == '`[only:/page/index.mu]'


def test_separator_variants():
    # default separator
    b = MicronBuilder()
    b.separator()
    assert b.build() == '\n-\n\n'

    # custom char, no surrounding breaklines
    b = MicronBuilder()
    b.separator('*', top_breakline=False, bottom_breakline=False)
    assert b.build() == '-*'

    # top only
    b = MicronBuilder()
    b.separator('#', top_breakline=True, bottom_breakline=False)
    assert b.build() == '\n-#'


def test_header_clear_breakline_and_str():
    b = MicronBuilder()
    b.header('Title', indent_level=3)
    assert b.build() == '\n>>>' + 'Title' + '\n'

    # indent_level less than 1 becomes 1
    b = MicronBuilder()
    b.header('T', indent_level=0)
    assert b.build() == '\n>' + 'T' + '\n'

    # clear and breakline
    b = MicronBuilder()
    b.clear().breakline()
    assert b.build() == '\n``\n'

    # __str__ proxies to build
    assert str(b) == b.build()
