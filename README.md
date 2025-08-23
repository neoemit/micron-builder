# micron-builder

**micron-builder** is a small Python library for building micron markup strings programmatically.  
It provides a fluent API for composing text fragments, headers, separators, and styles without manually handling all the Micron markup symbols.

---

## ✨ Features

- Fluent API for building Micron markup strings
- Support for:
  - **Text fragments** with color, background color, and formatting (bold, italic, underline)
  - **Headers** with indent levels
  - **Separators** and line breaks
  - **Links** (address + page)
  - **Alignment** (center, right)
  - **Padding** around text
- Works with raw strings or the built-in `Color` enum
- Easy to extend and compose

---

## 📦 Installation

```bash
pip install micron-builder
```

## 🚀 Usage

Here’s a quick example of how to use `MicronBuilder`:

```python
from micron import MicronBuilder
from micron.colors import Color

builder = (
    MicronBuilder()
    .header("Welcome!", indent_level=1)
    .text(
        "This is bold red text",
        bold=True,
        color=Color.RED,
    )
    .breakline()
    .text("Centered and underlined", center=True, underline=True)
    .separator("=")
    .text(
        "Clickable link",
        address_link="aaabbbcccddd",
        page_link="index.mu",
        italic=True,
    )
)

print(builder.build())
```

This would output Micron markup like:

```

>Welcome!
`Ff00`!This is bold red text`!`f

`c
`_Centered and underlined`_
`a
-=

`*`[Clickable link`aaabbbcccddd:/page/index.mu]`*
```

Which renders appropriately in Micron-compatible renderers.

New: use the raw(...) method to insert unescaped Micron markup directly

```python
from micron import MicronBuilder
from micron.colors import Color

builder = (
    MicronBuilder()
    .text("Some text", color=Color.GREEN)
    # raw() inserts the provided string exactly as-is into the output,
    # useful for injecting already-formed Micron markup.
    .raw("`!`Ff00This is raw micron markup`f`!")
)

print(builder.build())
```

This will include the raw markup verbatim in the output:

```
`F070Some text`f
`!`Ff00This is raw micron markup`f`!
```

## 🎨 Colors

Colors can be specified as:
- A **3-digit hex string** (e.g. `"f00"`, `"0ff"`)
- A `Color` enum value:

    ```python
    from micron.colors import Color

    MicronBuilder().text("Hello", color=Color.AQUA)
    ```

## 🛠 Development

Clone the repo and install in editable mode:
```bash
git clone https://github.com/neoemit/micron-builder.git
cd micron-builder
pip install -e .
```

Run tests (if you add them later):
```bash
pytest
```

## 📜 License

MIT License.

Feel free to use in your own projects.

## 🙌 Contributing

Pull requests, bug reports, and suggestions are welcome!

Open an issue or submit a PR on [GitHub](https://github.com/neoemit/micron).
