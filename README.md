# Jupyter GUI

Library for dynamically converting between Jupyter Notebook code cell and GUI :computer: :left_right_arrow: :video_game:

With Jupyter GUI, coders can represent their Python code as Task Widgets to non-coders, who then sees easy-to-run Task Widgets instead of code.

1) Coders code,

2) Jupyter GUI converts their code as Task Widgets, and

3) non-coders run these easy-to-run Task Widgets (or modify the parameters in the Task Widgets, which can also be converted back to code reflecting these changes).

## Install Jupyter GUI

**After launching Notebook with Simpli for the 1st time, please give it a minute to download GUI components in the background (you can see the progress in the command line output).**

### For Mac OS X

```bash
# Install brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Install git
brew install git

# Install Node.js and NPM
brew install node

# Download Jupyter GUI
https://github.com/KwatME/jupyter_gui.git

# Install Jupter GUI
cd jupytergui
pip install .
```

### For Linux

```bash
# Install git
sudo apt-get install git

# Install Node.js and NPM
sudo apt-get install nodejs npm

# Download Jupyter GUI
git clone https://github.com/KwatME/jupyter_gui.git

# Install Jupyter GUI
cd jupytergui
pip install .
```

### For Windows

```bash
:(
```

## Terminology

### Task

A Python function call

### Task Widget

GUI representation of a Task

### Task Entry

Entry specifying a Task in a JSON

### Simplify

To convert a Python function call into a Task; either by 1) specifying the Task via JSON; or 2) within a Notebook

### Jupyter GUI Icon

The button at the top of a Jupyter Notebook (left of Flip Icon); clicking it shows the Task List

### Flip Icon

The button at the top of a Jupyter Notebook (right of Simpli Icon); clicking it converts a code to a Task Widget, and vice versa

### Task List

The list of Tasks; appears after clicking the Simpli Icon or pressing 'Shift + X'

### Task Category

Task category in the Task List; determined by the function library of a Task

### Jupyter GUI Repository

The master Simpli directory (this repository)

### Jupyter GUI Library

The Simpli Python library within the Simpli Repository

## How Jupyter GUI Works

[Video](https://www.youtube.com/watch?v=4czT7CTxRDE) on how Simpli works.

## How to Simplify a code (Simpli automatically registers Simplified Tasks in the Task List)

### 1) From a Notebook cell

[Video](https://www.youtube.com/watch?v=qX099IM_y8c) on how to simplify code in a notebook cell.

Jupyter GUI can convert a Notebook cell with any function call and at least 1 line of comment into a Task Widget (Jupyter GUI requires 1 line of comment to serve as the unique ID for this Task in the Task List).

The function calls can return value or assign them to variables. Here are examples of each case:

without assignment:

```python
# Label
foo(arg1, arg2=value, ...)
```

with assignment:

```python
# Label
bar = foo(arg1, arg2=value, ...)
```

Jupyter GUI can also register different modalities of a function. Here is an example: If this function (a simple function to count numbers) exists,

```python
def count(min_, max_, by):

    numbers = []

    for i in range(min_, max_, by):
        print(i)
        numbers.append(i)

    return numbers
```

then making a cell with this code enables Jupyter GUI to convert this cell into a Task Widget, and register the Task in the Task List as 'Count Odds'.

```python
# Count Odds
count(1, 10, 2)
```

If you make another cell with this code (which can also be Simplified into a Task Widget), Jupyter GUI registers this Task as 'Count Evens'.

```python
# Count Evens
count(0, 10, 2)
```

Just like this, Jupyter GUI registered 2 modalities (Count Odds & Count Events) of the function count, and these Tasks Widgets for these modalities can be created just by selecting the Task in the Task List.

### 2) From a JSON

Jupyter GUI can also register Tasks specified in a JSON in the Task List, enabling users to insert these Tasks in the Notebook just by selecting them in the Task List.

Simplifying Tasks from JSON is useful when you want to register multiple Tasks at once.

To Simplify a Task, just make an Task Entry for the Task in a JSON load the JSON into Simpli.

This is an template for such Task Entry:

    {
        "library_path": "path/to/library/",  # Optional

        "tasks":  # Required
            [
                {
                    "function_path": "library.path.to.file.function",  # Required

                    "label": "Name of this Task (unique ID)",  # Optional (will be created based on function_path if not specified)

                    "description": "This Task performs ...",  # Optional


                    "required_args":  # Optional
                        [
                            {
                                "name": "x",  # Required if specifying required_args
                                "label": "The X",  # Optional if specifying required_args (user sees label instead of name in a Task Widget) (will be created based on name if not specified)
                                "description": "The X is ...",  # Optional if specifying required_args
                            },
                            # (may add more required_args)
                        ],

                    "default_args":  # Optional (users won't see these arguments in the Task Widget)
                        [
                            {
                                "name": "y",  # Required if specifying default_args
                                "value": "100",  # Required if specifying default_args (the default value [y=100 will be an argument when calling this function])
                            },
                            # (may add more default_args)
                        ],

                    "optional_args":  # Optional
                        [
                            {
                                "name": "z",  # Required if specifying optional_args
                                "label": "The Z",  # Optional if specifying optional_args (user sees label instead of name in a Task Widget) (will be created based on name if not specified)
                                "description": "The Z is ...",  # Optional if specifying optional_args
                            },
                            # (may add more optional_args)
                        ],

                    "returns":  # Optional
                        [
                            {
                                "label": "The A",  # Required
                                "description": "The A is ...",  # Optional if specifying returns
                            },
                            # (may add more returns)
                        ],

                    "other_information":  # Optional
                        {
                            # (add any information in in format: str: list)
                            "version": ["1.0.0"],
                            "server": ["Broad Institute"],
                            "tag": ["RNA", "Sequencing"],
                            # (may add more other_information)
                        },
                },
                # (may add more tasks)
            ]
    }

## How Jupyter GUI executes a function

Since each Task has library_path and function_path, Jupyter GUI can execute any function as this (function_path is split into library_name [everything up to the last . in the function_path] and the function_name [everything after the last . in the function_path]):

```python
# Append a library path
sys.path.insert(0, library_path)

# Import function
from library_name import function_name as function

# Run function
function(required_default_and_optional_args)
```

and_optional_args) \```
