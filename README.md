# GPTize

GPTize is a Python script that helps you include only relevant files from 
a repository (with path context) for use as input to a generative AI 
prompt. 

By default it ignores anything in the specified path's .gitignore file.
It walks the directory prompting the user to include or exclude each file,
then outputs the content of the relevant files in a markdown format that
includes the filename and path, suitable for input to LLMs.

The tool saves a .gptignore in the directory it is invoked from. You can
load the .gptignore to repeat your previous selection with updated code
after saving changes.

## Installation

No installation is required. Just download the script and run it using 
Python.

## Usage

```
python gptize.py [--load-gptignore] [--ignore-gitignore] <path>
```

- `--load-gptignore`: Load the .gptignore file instead of prompting for 
each file.
- `--ignore-gitignore`: Ignore the .gitignore file and include all files.
- `<path>`: Path to the repository to be processed.

## Examples

1. To choose the files interactively:

```
python gptize.py /path/to/repo
```

This command will process the files in the repository located at 
`/path/to/repo`, prompting the user to include or exclude each file. Files 
that are excluded will be added to the .gptignore file.

2. To run the script again with the --load-gptignore flag and save the 
output to prompt.md:

```
python gptize.py --load-gptignore /path/to/repo > prompt.md
```

This command will process the files in the repository located at 
`/path/to/repo`, using the previously created .gptignore file, and save 
the content of relevant files in a markdown format to a file called 
prompt.md.

## Contributing

Please feel free to submit issues or pull requests to improve this script.

## License

This project is in the public domain. There is no need to place any 
restrictions on its distribution or use.
