import os
import mimetypes
import argparse
import pathspec

def load_ignore_file(path, filename):
    ignore_path = os.path.join(path, filename)
    if os.path.isfile(ignore_path):
        with open(ignore_path, "r") as ignore_file:
            return pathspec.PathSpec.from_lines("gitwildmatch", ignore_file)
    return None

def is_ignored(ignore_spec, file_path):
    return ignore_spec and ignore_spec.match_file(file_path)

def gptize(path, load_gptignore, ignore_gitignore):
    files_to_print = []

    gptignore_spec = None if not load_gptignore else load_ignore_file(path, ".gptignore")
    gitignore_spec = None if ignore_gitignore else load_ignore_file(path, ".gitignore")

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        rel_root = os.path.relpath(root, path)
        for file in files:
            rel_filepath = os.path.join(rel_root, file)
            if is_ignored(gptignore_spec, rel_filepath) or is_ignored(gitignore_spec, rel_filepath):
                continue
            if not gptignore_spec:
                inc = input(f"include {rel_filepath}? (Y/n): ").strip().lower()
                if inc == "n":
                    with open(os.path.join(path, ".gptignore"), "a") as gptignore_file:
                        gptignore_file.write(rel_filepath + "\n")
                    continue
            filepath = os.path.join(root, file)
            mimetype, _ = mimetypes.guess_type(filepath)
            if mimetype and not mimetype.startswith("application"):
                with open(filepath, "r") as f:
                    content = f.read()
                files_to_print.append((rel_filepath, mimetype.split('/')[1], content))
    for rel_filepath, mime_subtype, content in files_to_print:
        print(f"**{rel_filepath}**")
        print(f"```{mime_subtype}\n{content}\n```")

def main():
    parser = argparse.ArgumentParser(description="Include only relevant files from a repo (with path context) for use as input to a generative AI prompt.")
    parser.add_argument("path", help="Path to the repo to be processed.", type=str)
    parser.add_argument("--load-gptignore", help="Load the .gptignore file instead of prompting for each file.", action="store_true")
    parser.add_argument("--ignore-gitignore", help="Ignore the .gitignore file and include all files.", action="store_true")
    args = parser.parse_args()
    gptize(args.path, args.load_gptignore, args.ignore_gitignore)

if __name__ == "__main__":
    main()
