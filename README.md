# Simpli
Code <== Simpli ==> GUI Widget (in Jupyter Notebook)

---
## Install Simpli

### For Mac OS X
```bash
# Install brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Install git
brew install git

# Download simpli
git clone https://github.com/UCSD-CCAL/simpli.git

# Install simpli
cd simpli
pip install .
```


### For Linux
```bash
# Install git
sudo apt-get install git

# Download simpli
git clone https://github.com/UCSD-CCAL/simpli.git

# Install simpli
cd simpli
pip install .
```

### For Windows
```bash
:(
```

### Start (or restart) Jupyter Notebook and - enjoy __:)__






















TODO: clena up and incoorporate the doc below


How Simpli Works
Terminology
Notebook Package
A package of resources and jupyter notebooks that allows
Simpli Repository
The master Simpli folder
Simpli Library
The Simpli folder within the repository.
Simpli Icon
The widget button (with a lightning bolt) at the top of a jupyter notebook.
Task List
The list of available task that appears after clicking the icon or pressing “shift + x”.
Task Categories
The categories tasks are organized into in the task list. Task categories are determined by the location of the function that is being simplified. Functions that live in the same .py file will be in the same category in the task list.
Task Widget
One or multiple functions wrapped into a single execution widget user interface.
Simplify
To wrap one or multiple functions as a task.
Input Field
A text entry box for users to enter values for a required argument (defined in the .json) in widgets.
Input Field Label
The text in an input field that tells users what type of input is required by the widget.
Input Help Icon
The question mark box beside an input field that displays descriptions of what the input field requires.
Output Field
A text entry box for users to enter a variable name in which the output of a widget will be saved.
Output Field Label
The text in an output field that tells users what type of output will be produced by the widget.
Output Help Icon
The question mark box beside an output field that displays descriptions of output will be produced by the widget.
Run Button
The button marked “RUN” on a widget. When pressed the run button will execute the wrapped function or functions with the input and output values the user has provided.
Task Information
The text that describes what a task does. The task information can be found on the side panel of the task list when a task is selected, and on the right side of task that has been added to a notebook.
Introduction
Simpli creates a simple user interface for functions using json files. Simpli reads json files to create the user interfaces of widgets and executes the functions those widgets call. When you install Simpli, it creates the following file structure in your home directory:

HOME
.simpli
json
simpli.json
COMPILED.json

The Simpli.json and COMPILED.json files you see in the file structure above are actually links to the real json files, which sit in the Simpli library in your python packages directory. The functions described in the simpli.json are in a .py file also found in the Simpli library.
The Simpli .json
When Simpli looks for json files to read it goes to HOME/.simpli/jsons to find them. The .json file tells Simpli where to look for the functions it describes and how to make widget for those functions. Here is an example of a json that Simpli could read:

{
  "library_path": "path.to.grocery_library",
  "tasks": [
    {
      "label": "Calculate Grocery Costs",
      "function_path": "ralphs.christmas_shopping.calculate_grocery_costs",
      "required_args": [
        {
          "arg_name": “items",
           "label": "Items to buy"
        },
        {
          "arg_name": "cost_of_each",
          "label": "Cost of each item"
        }
      ],
      "default_args": [
        {
          "arg_name": "sales_tax",
          "value": ".08"
        }
      ],
      "returns": [
        {
          "label": "cost_of_groceries"
        },
      ]
    }
  ]
}

library_path and function_path in .json

When Simpli is reading a .json file, it inserts library_path into the path of your notebook environment (see # Append a library path below). Then Simpli splits the function_path into two parts: the library_name (everything up to the last . in the function_path) and the function_name (everything after the last . in the function_path). Then Simpli imports the function_name from the library_name (see # Import function below).

# Append a library path
sys.path.insert(0, library_path)
# Import function
from {} import  as function


'.format(library_name, function_name

Normally, the library_path will be the path to the library that contains the function you want to wrap in the .json and the function_path will be the path to the function in that library.  But there are exceptions. For example, if you want to wap function_x in a .json and function_x is inside, or imported in, the __init__.py file of the library_z, your library_path would be “path.to.library_z” and your function_path would be “function_x”. This will work as well.
required_args in .json
 All the required_args in a .json are shown as input fields in the Simpli widget that .json describes. Usually, the required_args section of the .json include arguments of the function that don’t have predefined values.
default_args in .json
The user interface of this widget with not show an input field for sales tax, because it’s a default argument. And when the calculate_grocery_costs function runs, it will use .08 as the sales tax. However, if a function has an argument with a default value, you can add this argument to the required_args section of the .json, instead of the default_args section, to give the user the ability to change the value for that argument.
labels in the .json
The values for the “labels” in the .json above serve as the title and text in the input and output fields of the widget this .json will create. For example, the label “Calculate Grocery Costs” will be the title of this widget and one of the input fields will say “Items to buy”.

