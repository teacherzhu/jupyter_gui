// Add shim to support Jupyter 3.x and 4.x
var Jupyter = Jupyter || IPython || {};
Jupyter.notebook = Jupyter.notebook || {};
var done_init = false;
var AUTOEXEC_FLAG = "# !AUTOEXEC";

/**
 * Wait for kernel and then init notebook widgets
 */
var wait_for_kernel = function(id) {
    if (!done_init && Jupyter.notebook.kernel) {
        notebook_init_wrapper();
    } else if (done_init) {
        clearInterval(id);
    }
};
/**
/**
 * Initialize SimpleX Notebook from the notebook page
 */
var notebook_init_wrapper = function() {
    if (!done_init && Jupyter.notebook.kernel) {
        try {
            // Call the core init function
            launch_init();

            // Mark init as done
            done_init = true;
        } catch (e) {
            console.log(e);
            wait_for_kernel();
        }
    }
};


var launch_init = function() {
    auto_run_widgets();
    add_menu_options();
    init_shortcuts();

    // Hide the loading screen
    setTimeout(function() {
        $(".loading-screen")
            .hide("fade");
    }, 100);
};

/**
 * Automatically run all SimpleX widgets on INITIALIZATION
 */
var auto_run_widgets = function() {
    console.log("auto_run_widgets");
    require(function() {
        $.each($(".cell"), function(index, val) {
            if ($(val)
                .html()
                .indexOf(AUTOEXEC_FLAG) > -1) {
                toSimpleXCell(null, index);
            }
        });
    });
};

var add_menu_options = function() {
    // Add SimpleX "cell type" if not already in menu
    var dropdown = $("#cell_type");
    var gpInDropdown = dropdown.find("option:contains('SimpleX')")
        .length > 0;
    if (!gpInDropdown) {
        dropdown.append(
            $("<option value='code'>SimpleX</option>")
        );

        dropdown.change(function(event) {
            var type = $(event.target)
                .find(":selected")
                .text();
            if (type === "SimpleX") {
                var former_type = Jupyter.notebook.get_selected_cell()
                    .cell_type;
                toSimpleXCell(former_type);
            }
        });

        // Reverse the ordering of events so we check for ours first
        $._data($("#cell_type")[0], "events")
            .change.reverse();
    }

    // add to Cell -> Cell Type -> SimpleX
    var cellMenu = $("#change_cell_type");
    var gpInMenu = cellMenu.find("#to_simplex")
        .length > 0;
    if (!gpInMenu) {
        cellMenu.find("ul.dropdown-menu")
            .append(
                $("<li id='to_simplex' title='Insert a SimpleX widget cell'><a href='#'>SimpleX</a></option>")
                .click(function() {
                    toSimpleXCell();
                })
            );
    }

    // add to toolbar
    var addButton = $('<div class="btn-group" id="insert_simplex_below"><button class="btn btn-default" title="insert SimpleX cell below"><i class="fa-plus-square-o fa"></i></button></div>');
    addButton.click(function() {
        showLibraryPanel();
        // Jupyter.notebook.insert_cell_below();
        // Jupyter.notebook.select_next();
        // toSimpleXCell();
    });
    $("#insert_above_below")
        .after(addButton);
};

var init_shortcuts = function() {
    // Initialize the SimpleX cell type keyboard shortcut
    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('shift-x', {
        help: 'to SimpleX',
        help_index: 'cc',
        handler: function() {
            showLibraryPanel();
            return false;
        }
    });

    // Initialize the undo delete keyboard shortcut
    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('z', {
        help: 'undo cell/widget deletion',
        help_index: 'cc',
        handler: function() {
            undelete_cell_or_widget();
            return false;
        }
    });

    // Initialize the undo delete button
    var undeleteCell = $('#undelete_cell a');
    undeleteCell.on("click", function(event) {
        undelete_cell_or_widget();
    });
}

/**
 * Undo deleting last set of cells/widgets
 */
var undelete_cell_or_widget = function() {
    // make sure there are deleted cells to restore
    if (Jupyter.notebook.undelete_backup == null)
        return;

    var backup = Jupyter.notebook.undelete_backup;
    var startIndex = Jupyter.notebook.undelete_index;
    var endIndex = startIndex + backup.length;
    var indices = _.range(startIndex, endIndex);

    // reinsert deleted cells appropriately
    Jupyter.notebook.undelete_cell();
    for (var i in indices) {
        var cell = $(".cell")[i];
        if ($(cell)
            .html()
            .indexOf(AUTOEXEC_FLAG) > -1) {
            toSimpleXCell(null, i);
        }
    }
};

var toSimpleXCell = function(formerType, index, simplex_data) {
    var dialog = require('base/js/dialog');
    if (index === undefined) {
        // using selected cell
        index = Jupyter.notebook.get_selected_index();
    }

    cell = Jupyter.notebook.get_cell(index);
    // TODO Define cell change internal function
    var cellChange = function(cell) {
        // // Get the auth widget code
        var code = AUTOEXEC_FLAG + `
from simplex.taskmanager import TaskManager
import json, os, matplotlib

%matplotlib inline

# load wrapper
config = json.loads('''${simplex_data}''')
task_manager = TaskManager(config, globals(), locals(), os.getcwd())

def set_globals():
    task_manager.global_n = globals()
    for name, value in task_manager.output.items():
        globals()[name] = value
        # exec('global {}'.format(name), globals())
        # exec('{} = value'.format(name))

# register callback
if (set_globals not in get_ipython().events.callbacks['post_run_cell']):
    get_ipython().events.register('post_execute', set_globals)

# make and show widget
task_view = task_manager.create_task_view(task_manager.tasks[0])
task_view.createPanel()
`;

        // Put the code in the cell
        cell.code_mirror.setValue(code);
        cell.execute();

        // show widget when executed

        function setupWidget(id) {
            // hide code immediately
            cell.input.addClass("simplex-hidden");

            // clear output of selected cell
            Jupyter.notebook.clear_output();

            // show widget upon finished execution
            if (cell.element.find(".my-panel")
                .length > 0) {
                clearInterval(id);
                $("[data-toggle='tooltip']")
                    .tooltip();

                // wait for widget to fully render before showing
                setTimeout(function() {
                    cell.element.find(".widget-area")
                        .height(cell.element.find(".my-panel")
                            .height());
                }, 300);

            }
        };

        var setupWidgetInterval = setInterval(function() {
            setupWidget(setupWidgetInterval);
        }, 100);

    };

    // Define cell type check
    var typeCheck = function(cell) {
        var cell_type = cell.cell_type;
        if (cell_type !== "code") {
            Jupyter.notebook.to_code(index);
        }
        setTimeout(function() {
            cellChange(cell);
        }, 10);
    };

    // Prompt for change if the cell has contents and
    // doesnt start with autoexec flag
    var contents = cell.get_text()
        .trim();

    if (contents !== "" && contents.indexOf(AUTOEXEC_FLAG) < 0) {
        dialog.modal({
            notebook: Jupyter.notebook,
            keyboard_manager: Jupyter.notebook.keyboard_manager,
            title: "Change to SimpleX Cell?",
            body: "Are you sure you want to change this to a SimpleX cell? This will cause " +
                "you to lose any code or other information already entered into the cell.",
            buttons: {
                "Cancel": {
                    "click": function() {
                        if (formerType) $("#cell_type")
                            .val(formerType)
                            .trigger("change");
                    }
                },
                "Change Cell Type": {
                    "class": "btn-warning",
                    "click": function() {
                        typeCheck(cell);
                    }
                }
            }
        });
    } else {
        typeCheck(cell);
    }
};

var STATIC_PATH = location.origin + Jupyter.contents.base_url + "nbextensions/simplex/resources/";

define([
    'base/js/namespace',
    'base/js/events',
    'jquery',
    STATIC_PATH + 'librarymodal.js'
], function(Jupyter, events) {
    function load_ipython_extension() {
        // custom CSS
        $('head')
            .append(
                $('<link />')
                .attr('rel', 'stylesheet')
                .attr('type', 'text/css')
                .attr('href', STATIC_PATH + 'theme.css')
            );

        // Wait for the kernel to be ready and then initialize the widgets
        var interval = setInterval(function() {
            wait_for_kernel(interval);
        }, 500);
    }

    return {
        load_ipython_extension: load_ipython_extension
    };
});
