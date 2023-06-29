import os
from dataclasses import dataclass
from typing import Callable, List, Union


@dataclass
class File:
    name: str
    content_length: int


@dataclass
class Directory:
    name: str
    nodes: List[Union['File', 'Directory']]


def calculate_content_length(node: File | Directory) -> int:
    if isinstance(node, File):
        return node.content_length
    return sum(calculate_content_length(child_node) for child_node in node.nodes)

def get_repository_process_preview(root_path, should_ignore_fn: Callable):
    output = ''
    def build_node(parent_path, item):
        item_path = os.path.join(parent_path, item)

        if os.path.isdir(item_path):
            child_nodes = []

            for child_item in os.listdir(item_path):
                child_item_path = os.path.join(item_path, child_item)
                if not should_ignore_fn(child_item_path):
                    child_node = build_node(parent_path=item_path, item=child_item)
                    child_nodes.append(child_node)

            return Directory(name=item, nodes=child_nodes)
        else:
            with open(item_path, 'r', errors='ignore') as file:
                contents = file.read()
            return File(name=item, content_length=len(contents))

    def collect_node_output(node, indent: str, is_last: bool, format_fn: Callable):
        nonlocal output
        output += format_fn(node, indent, is_last)
        if isinstance(node, Directory):
            nodes_sort_by_content_length = sorted(node.nodes, key=calculate_content_length, reverse=True)
            for i, child_node in enumerate(nodes_sort_by_content_length):
                is_last_child = i == len(node.nodes) - 1
                child_indent = indent + ('    ' if is_last else '│   ')
                collect_node_output(child_node, child_indent, is_last_child, format_fn)


    root_node = build_node(parent_path=os.path.dirname(root_path), item=os.path.basename(root_path))
    total_characters = calculate_content_length(root_node)

    def tree_format(node: File | Directory, indent: str, is_last: bool) -> str:
        prefix = '└── ' if is_last else '├── '
        characters = calculate_content_length(node)
        percentage = characters / total_characters * 100
        return f'{indent}{prefix}{node.name} ({characters} characters) ({percentage:.2f}%)\n'

    collect_node_output(root_node, indent='', is_last=True, format_fn=tree_format)

    return output
