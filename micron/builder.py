from __future__ import annotations

from typing import List, Optional, Union
from .colors import Color


class MicronBuilder:
    """Fluent string builder for micron markup.

    This preserves the original small markup language semantics while
    providing clearer internal structure and helper methods.
    """

    def __init__(self) -> None:
        self.parts: List[str] = []

    # -- Public fluent API -------------------------------------------------
    def text(
        self,
        content: str,
        *,
        color: Optional[Union[str, Color]] = None,
        bgcolor: Optional[Union[str, Color]] = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        center: bool = False,
        right: bool = False,
        padding: int = 0,  # 1 extends horizontally, from 2 onwards it does vertically
        address_link: Optional[str] = None,
        page_link: str = "index.mu",
    ) -> "MicronBuilder":
        """
        Add a text fragment with optional styles and links.
        """

        fragment = content or ""

        if address_link:
            fragment = self._attach_address_link(fragment, address_link, page_link)

        padding_block = "\n" * padding
        fragment = f"{padding_block}{fragment}{padding_block}"

        # style wrappers: order matters (keep same order as original)
        if bold:
            fragment = self._wrap(fragment, "!", "`", "`")
        if italic:
            fragment = self._wrap(fragment, "*", "`", "`")
        if underline:
            fragment = self._wrap(fragment, "_", "`", "`")

        if color:
            fragment = self._wrap_color(fragment, color, prefix="F", suffix="f")

        if bgcolor:
            fragment = self._wrap_color(fragment, bgcolor, prefix="B", suffix="b")

        # alignment wrappers (kept in original order: center then right)
        if center:
            fragment = f"\n`c\n{fragment}\n`a"

        if right:
            fragment = f"\n`r\n{fragment}\n`a"

        self.parts.append(fragment)
        return self

    def separator(self, char: str = "", top_breakline: bool = True, bottom_breakline: bool = True) -> "MicronBuilder":
        """Append a separator line. Preserves original newline counts."""
        top = "\n" if top_breakline else ""
        bottom = "\n" if bottom_breakline else ""
        # original behavior used bottom*2
        self.parts.append(f"{top}-{char}{bottom * 2}")
        return self

    def header(self, content: str = "", indent_level: int = 1) -> "MicronBuilder":
        """Append a header line where indent is represented by repeated '>' chars."""
        level = max(1, int(indent_level))
        self.parts.append(f"\n{('>' * level)}{content}\n")
        return self
    
    def raw(self, content: str) -> "MicronBuilder":
        """Append raw content without any processing."""
        self.parts.append(content)
        return self

    def clear(self) -> "MicronBuilder":
        self.parts.append("\n``")
        return self

    def breakline(self) -> "MicronBuilder":
        self.parts.append("\n")
        return self

    def build(self) -> str:
        return "".join(self.parts)

    def __str__(self) -> str:  # pragma: no cover - convenience
        return self.build()

    # -- Internal helpers --------------------------------------------------
    @staticmethod
    def _wrap(text: str, marker: str, prefix: str = "`", suffix: str = "`") -> str:
        """Wrap text with a simple marker using given prefix/suffix.

        Example: _wrap('x', '!', '`', '`') -> '`!x`!'
        """
        return f"{prefix}{marker}{text}{suffix}{marker}"

    @staticmethod
    def _wrap_color(text: str, color: Union[str, Color], prefix: str = "F", suffix: str = "f") -> str:
        """Wrap text with a color/background color marker. Accepts Color enum or raw string.

        Preserves original behavior for how color values are embedded.
        """
        hex_value = color.value if isinstance(color, Color) else color
        return f"`{prefix}{hex_value}{text}`{suffix}"

    @staticmethod
    def _attach_address_link(fragment: str, address_link: str, page_link: str) -> str:
        """Attach an address link to the fragment following original rules.

        If fragment is non-empty, append a trailing backtick before building the
        link fragment. Otherwise build link with an empty inner label.
        """
        inner = f"{fragment}`" if fragment else ""
        return f"`[{inner}{address_link}:/page/{page_link}]"

