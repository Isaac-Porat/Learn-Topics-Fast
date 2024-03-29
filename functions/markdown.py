import os

def saveMarkdown(text: str, filename: str = "output.md"):
    markdown_output_path = "downloads/markdown-output"
    os.makedirs(markdown_output_path, exist_ok=True)
    filepath = os.path.join(markdown_output_path, filename)
    with open(filepath, 'w') as file:
        file.write(text)
    return filepath


