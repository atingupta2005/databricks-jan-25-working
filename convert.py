import os
import glob
from nbformat import v4 as nbf
import nbformat

def convert_md_to_notebook(md_file):
    # Read the markdown file content
    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Create a new Jupyter notebook (using nbformat)
    notebook = nbf.new_notebook()
    notebook.cells.append(nbf.new_markdown_cell(markdown_content))

    # Define the output notebook file path (same directory as the .md file)
    output_filename = os.path.splitext(md_file)[0] + '.ipynb'
    
    # Write the notebook to the file using nbformat.writes
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(nbformat.writes(notebook))  # Convert notebook to JSON string and write to file

    print(f"Converted {md_file} to {output_filename}")

def main():
    # Find all .md files recursively
    md_files = glob.glob('**/*.md', recursive=True)

    # Convert each markdown file to a notebook
    for md_file in md_files:
        convert_md_to_notebook(md_file)

if __name__ == "__main__":
    main()
