from micron import MicronBuilder, Color

def header(text: str):
    builder = (
        MicronBuilder()
        .separator('=', top_breakline=False, bottom_breakline=False)
        .text(text, bold=True, center=True, color=Color.YELLOW, bgcolor=Color.BLUE, padding=2)
        .separator('=')
    )
    return str(builder)

print(header("Micron Colors Example"))

rabbit = r'''
                          .".
                         /  |
                        /  /
                       / ,"
           .-------.--- /
          "._ __.-/ o. o\  
             "   (    Y  )
                  )     /
                 /     (
                /       Y
            .-"         |
           /  _     \    \ 
          /    `. ". ) /' )
         Y       )( / /(,/
        ,|      /     )
       ( |     /     /
        " \_  (__   (__
            "-._,)--._,)

'''

builder = (
    MicronBuilder()
    .text('Error!', color=Color.PINK, bgcolor=Color.BROWN, bold=True)
    .text(' ')
    .text('Success!', color=Color.LIME, italic=True)
    .separator('~')
    .text('Info', color=Color.BLUE, underline=True, center=True)
    .breakline()
    .separator()
    .header('Title')
    .text('Right alignment?', right=True)
    .header('Subtitle', indent_level=2)
    .text('This is a text fragment with styles', color=Color.PURPLE)
    .breakline()
    .text('With micron, you can control layout and presentation', bgcolor=Color.WHITE, color=Color.BLACK, center=True, padding=2)
    .text('... and foreground colors', bgcolor=Color.GREEN, right=True, padding=2)
    .breakline()
    .text('Links are also supported', color=Color.CYAN, padding=1)
    .breakline()
    .text('This is a link', address_link='123123123', color=Color.TOMATO, underline=True, padding=1)
    .raw(rabbit)
)

print(str(builder)) # or "print(builder.build())"
