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
 * Initialize JupyterX Notebook from the notebook page
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

/**
 * Automatically run all GenePattern widgets on INITIALIZATION
 */
var auto_run_widgets = function() {
    console.log("auto_run_widgets");
    require(function() {
        $.each($(".cell"), function(index, val) {
            if ($(val).html().indexOf(AUTOEXEC_FLAG) > -1) {
                toJupyterXCell(null, index);
            }
        });
    });
};

/**
 * Undo deleting last set of cells/widgets
 */
var undelete_cell_or_widget = function() {
    var backup = Jupyter.notebook.undelete_backup;
    var startIndex = Jupyter.notebook.undelete_index;
    var endIndex = startIndex + backup.length;
    var indices = _.range(startIndex, endIndex);

    // reinsert deleted cells appropriately
    Jupyter.notebook.undelete_cell();
    for (var i in indices) {
        var cell = $(".cell")[i];
        if ($(cell).html().indexOf(AUTOEXEC_FLAG) > -1) {
            toJupyterXCell(null, i);
            console.log('yay');
        }
    }
}

var add_menu_options = function() {

    // Add GenePattern "cell type" if not already in menu
    var dropdown = $("#cell_type");
    var gpInDropdown = dropdown.find("option:contains('JupyterX')").length > 0;
    if (!gpInDropdown) {
        dropdown.append(
            $("<option value='code'>JupyterX</option>")
        );

        dropdown.change(function(event) {
            var type = $(event.target).find(":selected").text();
            if (type === "JupyterX") {
                var former_type = Jupyter.notebook.get_selected_cell().cell_type;
                toJupyterXCell(former_type);
            }
        });

        // Reverse the ordering of events so we check for ours first
        $._data($("#cell_type")[0], "events").change.reverse();
    }

    var cellMenu = $("#change_cell_type");
    var gpInMenu = cellMenu.find("#to_jupyterx").length > 0;
    if (!gpInMenu) {
        cellMenu.find("ul.dropdown-menu")
            .append(
                $("<li id='to_jupyterx' title='Insert a JupyterX widget cell'><a href='#'>JupyterX</a></option>")
                .click(function() {
                    toJupyterXCell();
                })
            );
    }
}

var toJupyterXCell = function(formerType, index) {
    var dialog = require('base/js/dialog');
    if (index === undefined) {
        // using selected cell
        index = Jupyter.notebook.get_selected_index();
    }
    cell = Jupyter.notebook.get_cell(index);

    // TODO Define cell change internal function
    var cellChange = function(cell) {

        // // Get the auth widget code
        var code = AUTOEXEC_FLAG + "\n\
from my_extension.chain import Chain\n\
import json, os\n\n\
# load wrapper\n\
json_filepath = '/Users/ckmah/Documents/jupyter_x/ccal.json'\n\
with open(json_filepath, 'r') as f:\n\
    config = json.load(f)\n\n\
controller = Chain(config, globals(), locals(), os.getcwd())\n\
beadview = controller.createBeadView(controller.beads[0])\n\
beadview.createPanel()";

        // Put the code in the cell
        cell.code_mirror.setValue(code);

        // TODO check for running state
        function isWidgetPresent() {
            return cell.element.find(".my-panel").length > 0;
        }

        // function isRunning() {
        //     return cell.element.hasClass("running") }

        var widgetPresent = isWidgetPresent();
        // var running = isRunning();

        // function ensure_widget() {
        //     // if (!widgetPresent && !running) {
        //     if (!widgetPresent) {
        //         function hideCode() {
        //             if (cell.length > 0) {
        //                 cell.input
        cell.input.css("height", "0")
            .css("overflow", "hidden");
        //         } else {
        //             setTimeout(hideCode(), 10);
        //         }
        //     }
        //     hideCode();

        cell.execute();
        //     clearTimeout();
        // }
        // if (!widgetPresent) {
        //     setTimeout(function() {
        //         widgetPresent = isWidgetPresent();
        //         ensure_widget();
        //     }, 500);
        // }
        // }
        // ensure_widget();
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
    var contents = cell.get_text().trim();
    if (contents !== "" && contents.indexOf(AUTOEXEC_FLAG) < 0) {
        dialog.modal({
            notebook: Jupyter.notebook,
            keyboard_manager: Jupyter.notebook.keyboard_manager,
            title: "Change to JupyterX Cell?",
            body: "Are you sure you want to change this to a JupyterX cell? This will cause " +
                "you to lose any code or other information already entered into the cell.",
            buttons: {
                "Cancel": {
                    "click": function() {
                        if (formerType) $("#cell_type").val(formerType).trigger("change");
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

var init_shortcuts = function() {
    // Initialize the JupyterX cell type keyboard shortcut
    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('g', {
        help: 'to JupyterX',
        help_index: 'cc',
        handler: function() {
            toJupyterXCell();
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
    var undeleteCell = $('#undelete_cell');
    undeleteCell.on("click", function(event) {
        undelete_cell_or_widget();
    });
}

var launch_init = function() {
    auto_run_widgets();
    add_menu_options();
    init_shortcuts();

    $(document).ready(function() {
        // enable tooltips
        $("[data-toggle='tooltip']").tooltip();
    });

    // Hide the loading screen
    setTimeout(function() {
        $(".loading-screen").hide("fade");
    }, 100);
};

var STATIC_PATH = location.origin + Jupyter.contents.base_url + "nbextensions/my_extension/";

define([
    "base/js/namespace",
    'base/js/events',
    "jquery",
    STATIC_PATH + "task.js"
], function(Jupyter, events) {

    // NOTE: CSS injection point
    function load_ipython_extension() {
        // custom CSS
        $('head').append(
            $('<link />')
            .attr("rel", "stylesheet")
            .attr("type", "text/css")
            .attr('href', STATIC_PATH + 'theme.css'),
            $('<link />')
            .attr("rel", "stylesheet")
            .attr("type", "text/css")
            .attr('href', 'https://fonts.googleapis.com/icon?family=Material+Icons')
        );
        $('head').append(
            $('<script/>')
            .attr('type', 'text/javascript')
            .html('$("[data-toggle=\'tooltip\']").tooltip()'));
        // Wait for the kernel to be ready and then initialize the widgets
        var interval = setInterval(function() {
            wait_for_kernel(interval);
        }, 500);
    }

    return {
        load_ipython_extension: load_ipython_extension
    };
});
