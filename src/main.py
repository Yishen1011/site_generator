import os, shutil, pathlib, sys
from markdown_to_html import markdown_to_html_node

def main():

    args = sys.argv
    if len(sys.argv) > 2:
        print("Error: Too many arguments.")
        print("Usage: ./main.sh <basepath>")
        print(sys.argv)
        sys.exit(1)
    if len(args) == 1:
        basepath = "/"
    else:
        basepath = args[1]
    print(f"Base path: {basepath}\n")

    source_path = "static"
    destination_path = "docs"
    copy_content(source_path, destination_path)
    # generate_page("content/index.md", "template.html", "public/index.html", basepath)
    # generate_pages_recursive("content", "template.html", "public", basepath)
    generate_pages_recursive("content", "template.html", "docs", basepath)

def copy_content(source, destination):
    print("Copying files from source: {source} to destination: {destination}")
    # It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_content_aux(source, destination)
    print("")

def copy_content_aux(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination)
            print(f"Successfully copied {file_path} into {destination}")
        elif os.path.isdir(file_path):
            destination_file_path = os.path.join(destination, filename)
            os.mkdir(destination_file_path)
            copy_content_aux(file_path, destination_file_path)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read markdown file from_path and store the contents in variable
    with open(from_path) as p:
        from_path_content = p.read()
    # Read template file at template path and store the contents in variable
    with open(template_path) as t:
        template_content = t.read()

    from_path_html = markdown_to_html_node(from_path_content).to_html()
    from_path_title = extract_title(from_path_content)
    basepath_href = 'href="' + basepath
    basepath_src = 'src="' + basepath

    replace_title = template_content.replace("{{ Title }}", from_path_title)
    replace_content = replace_title.replace("{{ Content }}", from_path_html)

    replace_href = replace_content.replace('href="/', basepath_href)
    full_html = replace_href.replace('src="/', basepath_src)

    dest_parent = os.path.dirname(dest_path)
    os.makedirs(dest_parent, exist_ok=True)

    with open(dest_path, "w") as g:
        g.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(file_path):
            print(f"Source File: {file_path}")
            name = pathlib.Path(filename).stem + ".html"
            dest_file = pathlib.Path(dest_dir_path) / name
            print(f"Destination File: {dest_file}")
            generate_page(file_path, template_path, dest_file, basepath)
            print(f"Successfully generated {file_path} into {name} using {template_path}\n")
        elif os.path.isdir(file_path):
            print(f"Source Folder: {file_path}")
            destination_file_path = os.path.join(dest_dir_path, filename)
            print(f"Destination Folder: {destination_file_path}\n")
            os.mkdir(destination_file_path)
            generate_pages_recursive(file_path, template_path, destination_file_path, basepath)

if __name__ == "__main__":
    main()
