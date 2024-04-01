import os
import shutil

from htmlnode import generate_page
from textnode import TextNode


def copytree(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)
    source_list = os.listdir(source)
    for d in source_list:
        if os.path.isfile(os.path.join(source, d)):
            shutil.copy(os.path.join(source, d), destination)
            continue
        copytree(os.path.join(source, d), os.path.join(destination, d))
    return


def main():
    copytree("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()
