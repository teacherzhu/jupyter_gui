// Add shim to support Jupyter 3.x and 4.x
var Jupyter = Jupyter || IPython || {};
Jupyter.notebook = Jupyter.notebook || {};
var isInitDone = false;
const AUTOEXEC_FLAG = "# !AUTOEXEC";

/**
 * Wait for notebook kernel to start before initializing extension.
 * @param  {number} id The id generated by the setInterval() function.
 */
const waitForKernel = function(id) {
  if (!isInitDone && Jupyter.notebook.kernel && Jupyter.notebook.kernel.is_connected()) {
    initWrapper(id);
  } else if (isInitDone) {
    clearInterval(id);
  }
};

/**
 * Wraps extension initialization function to keep trying to initialize until
 * @param  {number} id The id generated by the setInterval() function.
 */
const initWrapper = function(id) {
  if (!isInitDone && Jupyter.notebook.kernel && Jupyter.notebook.kernel.is_connected()) {
    try { // Call the core init function
      init();
      isInitDone = true;
    } catch (e) { // Keep trying init until kernel is started
      console.log(e);
      waitForKernel(id);
    }
  }
};

/**
 * Initializes the extension.
 */
const init = function() {
  setupCallbacks();
  autoRunWidgets();
  addMenuOptions();
  mapKeyboardShortcuts();

  // FIXME: figure out what this actually hides
  // Hide the loading screen
  setTimeout(function() {
    $(".loading-screen")
      .hide("fade");
  }, 100);

  console.log('SimpleX nbextension initialized.');
};

/**
 * Setup cell execution callbacks to the notebook kernel.
 */
const setupCallbacks = function() {
  var initCode =
    `
global task_manager

def init_task_manager():
    global os
    import os

    global json
    import json

    global Javascript
    from IPython.display import Javascript

    global matplotlib
    import matplotlib

    global TaskManager
    from simplex import TaskManager

    %matplotlib inline

    # Initialize a TaskManager
    global task_manager
    task_manager = TaskManager()

def sync_namespaces():
    '''
    Sync namespaces of this Notebook and SimpleX TaskManager.
    :return: None
    '''

    # Notebook namespace ==> TaskManager namespace
    global task_manager
    task_manager.update_simplex_namespace(globals())

    # TaskManager namespace ==> Notebook namespace
    for name, value in task_manager.simplex_namespace.items():
        globals()[name] = value

# Register post execute cell callback
if sync_namespaces not in get_ipython().events.callbacks['post_execute']:
    get_ipython().events.register('post_execute', sync_namespaces)

# Register kernel initialization callback
if (init_task_manager not in get_ipython().events.callbacks['shell_initialized']):
    get_ipython().events.register('shell_initialized', init_task_manager)

# Initial namespace sync
init_task_manager()
sync_namespaces()
`;

  // Kernel executes python code in background
  Jupyter.notebook.kernel.execute(initCode);

  // TODO: Initialize extension on kernel restart
  // Jupyter.notebook.kernel.restart(function() {
  //   waitForKernel();
  // });

  console.log('Called setupCallbacks()');
}


/**
 * Automatically run all SimpleX widgets on initialization.
 * TODO: Forms should 'remember' their input
 */
const autoRunWidgets = function() {
  console.log('Called autoRunWidgets()');
  $.each($(".cell"), function(index, value) {
    if ($(value).html().indexOf(AUTOEXEC_FLAG) > -1) {
      toSimpleXCell(null, index);
    }
  });
};

/**
 * Add menu options to notebook navbar and toolbar.
 */
const addMenuOptions = function() {
  const dropdown = $("#cell_type");
  const gpInDropdown = dropdown.find("option:contains('SimpleX')").length > 0;

  if (!gpInDropdown) {
    // Add SimpleX "cell type" to toolbar cell type dropdown menu
    dropdown.append($("<option value='code'>SimpleX</option>"));

    // Change cell to SimpleX cell type
    dropdown.change(function(event) {
      var type = $(event.target).find(":selected").text();
      if (type === "SimpleX") {
        var former_type = Jupyter.notebook.get_selected_cell().cell_type;
        showTasksPanel();
      }
    });

    // Reverse the ordering of events so we check for ours first
    $._data($("#cell_type")[0], "events").change.reverse();
  }

  // Add to notebook navbar dropdown menu.
  // Menu path: Cell -> Cell Type -> SimpleX
  const cellMenu = $("#change_cell_type");
  const gpInMenu = cellMenu.find("#to_simplex").length > 0;
  if (!gpInMenu) {
    cellMenu.find("ul.dropdown-menu").append(
      $("<li id='to_simplex' title='Insert a SimpleX widget cell'><a href='#'>SimpleX</a></option>")
      .click(function() {
        showTasksPanel();
      })
    );
  }

  // Add button for creating SimpleX cell to toolbar
  const addButton = $(
    '<div class="btn-group" id="insert_simplex_below"><button class="btn btn-default" title="insert SimpleX cell below"><i class="fa fa-th-large"></i></button></div>'
  );
  addButton.click(function() {
    Jupyter.notebook.insert_cell_below();
    Jupyter.notebook.select_next();
    showTasksPanel();
  });
  $("#insert_above_below").after(addButton); // add after insert cell button

  // Initialize the undo delete menu entry click function
  var undeleteCell = $('#undelete_cell a');
  undeleteCell.on("click", function(event) {
    undoDeleteCell();
  });
};

/**
 * Initialize custom keyboard shortcuts for SimpleX.
 */
const mapKeyboardShortcuts = function() {
  // Initialize the SimpleX cell type keyboard shortcut
  Jupyter.keyboard_manager.command_shortcuts.add_shortcut('shift-x', {
    help: 'to SimpleX',
    handler: function() {
      showTasksPanel();
      return false;
    }
  });

  // Initialize the undo delete keyboard shortcut
  Jupyter.keyboard_manager.command_shortcuts.add_shortcut('z', {
    help: 'undo cell/widget deletion',
    handler: function() {
      undoDeleteCell();
      return false;
    }
  });

  // Handle esc key
  $('body').keydown(function(event) {

    // Remove focus from active element
    if (event.keyCode == 27) {
      document.activeElement.blur();
    }

    // Close the library
    if (event.keyCode == 27 && $('#library-cancel-btn').length) {
      $('#library-cancel-btn').click();
      return;
    }
  });
}

/**
 * Undo deleting last set of cells/widgets.
 * FIXME: test if it actually works
 */
const undoDeleteCell = function() {
  // Make sure there are deleted cells to restore
  if (Jupyter.notebook.undelete_backup == null)
    return;

  var backup = Jupyter.notebook.undelete_backup;
  var startIndex = Jupyter.notebook.undelete_index;
  var endIndex = startIndex + backup.length;
  var indices = _.range(startIndex, endIndex);

  // Reinsert deleted cells appropriately
  Jupyter.notebook.undelete_cell();
  for (var i in indices) {
    var cell = $(".cell")[i];
    if ($(cell).html().indexOf(AUTOEXEC_FLAG) > -1) {
      toSimpleXCell(null, i);
    }
  }
};

/**
 * Converts indicated cell to SimpleX widget and hiding code input.
 * @param  {String} formerType   type of cell to be converted
 * @param  {number} index        index of cell in notebook
 * @param  {String} simplex_data stringified task JSON
 */
const toSimpleXCell = function(formerType, index, taskDict) {
  // Use index if provided. Otherwise index of currently selected cell.
  if (index === undefined) {
    index = Jupyter.notebook.get_selected_index();
  }

  cell = Jupyter.notebook.get_cell(index);

  var cellChange = function(cell) {
    // If taskDict is not passed, the cell is auto-executed.
    if (taskDict) {
      var code = AUTOEXEC_FLAG +
        `
# Make and show widget
task_view = task_manager.create_task_view(json.loads('''${taskDict}'''))
task_view.create()
      `;

      // Put the code in the cell
      cell.code_mirror.setValue(code);
    }

    cell.execute();

    function setupWidget(id) {
      // Hide code immediately
      cell.input.addClass("simplex-hidden");
      cell.element.find(".widget-area .prompt").addClass("simplex-hidden");

      // Show and manipulate widget upon finished execution
      if (cell.element.find(".form-panel").length > 0 && cell.element.find(".form-panel").outerHeight() > 50) {
        clearInterval(id);


        // Wait for widget to fully render before modifying it
        setTimeout(function() {
          // Show widget
          cell.element.find(".widget-area").height(cell.element.find(".panel-wrapper").outerHeight());

          // Enable javascript tooltips
          $("[data-toggle='tooltip']").tooltip();
        }, 200);
      }
    };

    // Wait for python execution
    var setupWidgetInterval = setInterval(function() {
      setupWidget(setupWidgetInterval);
    }, 50);

  };

  // Forces cell type to change to code before executing
  var typeCheck = function(cell) {
    var cell_type = cell.cell_type;
    if (cell_type !== "code") {
      Jupyter.notebook.to_code(index);
    }

    setTimeout(function() {
      // Clear output of selected cell
      cell.clear_output();
      cellChange(cell);
    }, 10);
  };

  // Prompt for change if the cell has contents and
  // doesnt start with autoexec flag
  var contents = cell.get_text().trim();
  if (contents !== "" && contents.indexOf(AUTOEXEC_FLAG) < 0) {
    // Use dialog modal Boostrap plugin
    var dialog = require('base/js/dialog');
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
    STATIC_PATH + 'tinysort.min.js',
    STATIC_PATH + 'tasksDialog.js'
], function(Jupyter, events) {
  function load_ipython_extension() {
    // Inject custom CSS
    $('head')
      .append(
        $('<link />')
        .attr('rel', 'stylesheet')
        .attr('type', 'text/css')
        .attr('href', STATIC_PATH + 'theme.css')
      );

    // Wait for the kernel to be ready and then initialize the widgets
    var interval = setInterval(function() {
      waitForKernel(interval);
    }, 500);
  }

  return {
    load_ipython_extension: load_ipython_extension
  };
});
