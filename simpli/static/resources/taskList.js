// Add shim to support Jupyter 3.x and 4.x
var Jupyter = Jupyter || IPython || {}
Jupyter.notebook = Jupyter.notebook || {};
const STATIC_LIB_PATH = location.origin + Jupyter.contents.base_url + "nbextensions/simpli/resources/";

/**
 * Holds all JSON for tasks.
 * @type {Array}
 */
var simpliTaskData = [];

/**
 * Index of selected task in reference to simpliTaskData.
 * @type {Number}
 */
var selectedIndex;

/**
 * Inner container of dialog for task selection.
 */
var taskListParent;

/**
 * Panel that displays selected task information.
 */
var rightPanel;

/**
 * Panel that lists all tasks detailed in simpliTaskData.
 */
var leftPanel;

/******************** MAIN FUNCTIONS ********************/
/** TODO: rename to task list
 * Creates dialog modal that user can select a task from.
 */
const showTaskList = function() {
  initTaskList();

  var dialog = require('base/js/dialog');
  dialog.modal({
    notebook: Jupyter.notebook,
    keyboard_manager: Jupyter.notebook.keyboard_manager,
    body: taskListParent
  });

  // Style parent after it renders
  var interval = setInterval(function() {
    if ($('#library-parent').length > 0) {
      var libParent = $('#library-parent');
      libParent.parent().addClass('library-modal-body');
      libParent.parents('.modal-content').find('.modal-header').addClass('library-modal-header');
      libParent.parents('.modal-content').find('.modal-footer').addClass('library-modal-footer');
      libParent.parents('.modal-dialog').addClass('library-modal-dialog').on('click', function(event) {
        event.preventDefault();
      });
      clearInterval(interval);
    }
  }, 100);
}

/**
 * Initialize panels inside task dialog and saves to taskListParent object.
 */
const initTaskList = function() {
  taskListParent = $('<div/>').attr('id', 'library-parent');

  // Display tasks elements
  leftPanel = $('<div/>')
    .addClass('library-left-panel')
    .addClass('pull-left')
    .addClass('col-xs-7')
    .appendTo(taskListParent);

  var leftPanelHeader = $('<h1/>')
    .addClass('library-left-panel-header')
    .html('Simpli Library')
    .appendTo(leftPanel);

  // Specifically to hold cards
  var leftPanelInner = $('<div/>')
    .addClass('library-left-panel-inner')
    .appendTo(leftPanel);

  // Define right panel
  rightPanel = $('<div/>')
    .attr('id', 'library-right-panel')
    .addClass('pull-right')
    .addClass('col-xs-5')
    .appendTo(taskListParent);

  renderRightPanel();
  renderTasks();
}

/******************** HELPER FUNCTIONS ********************/

/**
 * Create left panel showing list of tasks.
 */
var renderTasks = function() {
  console.log('Called renderTasks()');

  var loadText = $('<div/>')
    .addClass('library-load-text')
    .html('Loading...')
    .appendTo(leftPanel);

  // code to read library JSON files
  var code = 'print(json.dumps(mgr.tasks))';

  // Callback from
  var callback = function(out) {

    // Convert dictionary to stringified list
    var tasksDict = JSON.parse(out.content.text);
    simpliTaskData = Object.keys(tasksDict).map(function(key) {
      var task = tasksDict[key];
      task.label = key;
      return task;
    });

    // Sort tasks by package then function name alphabetically
    simpliTaskData.sort(function(a, b) {
      var alib = a.library_name.toLowerCase();
      var blib = b.library_name.toLowerCase();
      var alab = a.label.toLowerCase();
      var blab = b.label.toLowerCase();

      if (alib > blib) {
        return 1;
      } else if (alib == blib) {
        if (alab > blab) {
          return 1;
        } else if (alab < blab) {
          return -1;
        } else {
          return 0;
        }
      } else {
        return -1;
      }
    })

    // Hide loading text
    $(leftPanel).find('.library-load-text').addClass('library-load-text-hidden');

    // Render all tasks after loading text fades
    setTimeout(function() {
      var packages = {};
      for (var task of simpliTaskData) {
        var tasklib = task.library_name.toUpperCase();

        // Section headers = package names
        if (!(tasklib in packages)) {
          packages[tasklib] = 0;
          var packageHeader = $('<h3/>')
            .addClass('library-package-header')
            .html(tasklib);
          $(leftPanel).find('.library-left-panel-inner').append(packageHeader);
        }
        renderTask(task);
      }
      // $(leftPanel).find('.library-card').first().click();
    }, 200);

  }

  // Wait for kernel to not be busy
  var interval = setInterval(function() {
    // Use kernel to read library JSONs
    if (!Jupyter.notebook.kernel_busy) {
      clearInterval(interval);
      Jupyter.notebook.kernel.execute(code, {
        'iopub': {
          'output': callback
        }
      });
    }
  }, 10);

}

/**
.appendTo(taskListParent);
 * Render right panel and only updates inner content when necessary.
 */
const renderRightPanel = function() {
  // Render right panel
  var render = function() {

    // Parent container
    var taskInfo = $('<div/>')
      .attr('id', 'library-task-info');

    // Task title
    var taskHeading = $('<h2/>')
      .attr('id', 'library-task-heading')
      .appendTo(taskInfo);

    // Task library name
    var taskLibraryName = $('<h3/>')
      .attr('id', 'library-task-package')
      .appendTo(taskInfo);

    // Package author
    var taskAuthor = $('<div/>')
      .attr('id', 'library-task-author')
      .appendTo(taskInfo);

    // Task affiliation
    var taskAffiliation = $('<div/>')
      .attr('id', 'library-task-affiliation')
      .appendTo(taskInfo);

    // Task description
    var taskDescription = $('<div/>')
      .attr('id', 'library-task-description')
      .appendTo(taskInfo);

    // Select/cancel buttons
    var modalButtons = $('<div/>')
      .attr('id', 'library-button-group');
    var cancelButton = $('<button>')
      .attr('id', 'library-cancel-btn')
      .addClass('btn')
      .addClass('btn-default')
      .attr('data-dismiss', 'modal')
      .html('Cancel')
      .appendTo(modalButtons);
    var selectButton = $('<button>')
      .addClass('library-select-btn')
      .addClass('btn')
      .addClass('btn-default')
      .addClass('btn-primary')
      .attr('data-dismiss', 'modal')
      .html('Select')
      .on('click', function(event) {
        event.preventDefault();
        toSimpliCell(Jupyter.notebook.get_selected_index(), simpliTaskData[selectedIndex]);
      })
      .appendTo(modalButtons);

    taskInfo.appendTo(rightPanel);
    modalButtons.appendTo(rightPanel);
  };

  /**
   * Update existing rightPanel with currently selected task
   */
  var update = function() {
    // Parse and display task information
    var task = simpliTaskData[selectedIndex];

    $(rightPanel).find('#library-task-heading').html(task.label);
    $(rightPanel).find('#library-task-package').html(task.library_name);
    $(rightPanel).find('#library-task-author').html(task.author);
    $(rightPanel).find('#library-task-affiliation').html(task.affiliation);
    $(rightPanel).find('#library-task-description').html(task.description);
  }

  // Render if first call
  if (rightPanel.children().length == 0) {
    render();
  }
  // Update with selected task data
  else {
    update();
  }
}

/**
 * Render a card for a given task JSON string. Also responsible for triggering right panel display.
 * @param {String} task_data stringified JSON for a task
 */
const renderTask = function(task) {

  // Generate a card from given task_data
  var card = $('<a/>')
    .addClass('library-card')
    .on('click', function(event) {
      event.preventDefault();

      // click action
      selectedIndex = $(this).index('.library-card');
      renderRightPanel();

      // card selected style
      $('.library-card-selected').removeClass('library-card-selected');
      $(this).addClass('library-card-selected');

      $('.library-select-btn').addClass('library-select-btn-activated');
    })
    // Double click auto selects task
    .on('dblclick', function(event) {
      event.preventDefault();
      $('.library-select-btn').click();
    });

  // Label/title of method
  var label = $('<h4/>')
    .addClass('card-label')
    .html(task.label);

  // Structure elements appropriately
  label.appendTo(card);
  card.appendTo($('.library-left-panel-inner'));
}
