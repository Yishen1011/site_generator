import os, shutil
from markdown_to_html import markdown_to_html_node

def main():
    source_path = "static"
    destination_path = "public"
    copy_content(source_path, destination_path)
    generate_page("content/index.md", "template.html", "public/index.html")

def copy_content(source, destination):
    # It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_content_aux(source, destination)

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read markdown file from_path and store the contents in variable
    with open(from_path) as p:
        from_path_content = p.read()
    # Read template file at template path and store the contents in variable
    with open(template_path) as t:
        template_content = t.read()

    from_path_html = markdown_to_html_node(from_path_content).to_html()
    from_path_title = extract_title(from_path_content)

    updated_template = template_content.replace("{{ Title }}", from_path_title)
    full_html = updated_template.replace("{{ Content }}", from_path_html)

    dest_parent = os.path.dirname(dest_path)
    os.makedirs(dest_parent, exist_ok=True)

    with open(dest_path, "w") as g:
        g.write(full_html)

if __name__ == "__main__":
    main()
