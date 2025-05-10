def show_markdown(text):
    """
    Display the markdown text in a Jupyter notebook cell.
    """
    from IPython.display import display, Markdown
    display(Markdown(text))