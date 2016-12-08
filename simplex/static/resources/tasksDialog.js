// Add shim to support Jupyter 3.x and 4.x
var Jupyter = Jupyter || IPython || {}
Jupyter.notebook = Jupyter.notebook || {};
const STATIC_LIB_PATH = location.origin + Jupyter.contents.base_url + "nbextensions/simplex/resources/";

/**
 * Holds all JSON for tasks.
 * @type {Array}
 */
var simplexTaskData = [];

/**
 * Index of selected task in reference to simplexTaskData.
 * @type {Number}
 */
var selectedIndex;

/**
 * Inner container of dialog for task selection.
 */
var tasksPanelParent;

/**
 * Panel that displays selected task information.
 */
var rightPanel;

/**
 * Panel that lists all tasks detailed in simplexTaskData.
 */
var leftPanel;

/******************** MAIN FUNCTIONS ********************/
/**
 * Creates dialog modal that user can select a task from.
 */
const showTasksPanel = function() {
  initTasksPanel();

  var dialog = require('base/js/dialog');
  dialog.modal({
    notebook: Jupyter.notebook,
    keyboard_manager: Jupyter.notebook.keyboard_manager,
    body: tasksPanelParent
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
 * Initialize panels inside task dialog and saves to tasksPanelParent object.
 */
const initTasksPanel = function() {
  tasksPanelParent = $('<div/>').attr('id', 'library-parent');
  renderTasks();
}

/******************** HELPER FUNCTIONS ********************/

/**
 * Create left panel showing list of tasks.
 */
var renderTasks = function() {
  console.log('Called renderTasks()');

  // Display tasks elements
  leftPanel = $('<div/>')
    .addClass('library-left-panel')
    .addClass('pull-left')
    .addClass('col-xs-8')
    .appendTo(tasksPanelParent);

  // code to read library JSON files
  var code =
    `
from simplex import compile_tasks
print(compile_tasks())
  `;

  // Callback from
  var callback = function(out) {
    console.log(out);
    var tasksDict = JSON.parse(out.content.text);

    // Convert dictionary to stringified list
    simplexTaskData = Object.keys(tasksDict).map(function(key) {
      var task = tasksDict[key];
      task.label = key;
      return JSON.stringify(task);
    });

    // Generate all tasks
    for (var task of simplexTaskData) {
      renderTask(task);
    }

    // Try to select first one by default
    if ($(leftPanel).find('.library-card').length > 0) {
      $(leftPanel).find('.library-card').first().click();
    }
  }

  // Use kernel to read library JSONs
  Jupyter.notebook.kernel.execute(code, {
    'iopub': {
      'output': callback
    }
  });
}

/**
.appendTo(tasksPanelParent);
 * Render right panel and only updates inner content when necessary.
 */
const renderRightPanel = function() {

  // Parse and display task information
  var task = JSON.parse(simplexTaskData[selectedIndex]);

  // Render right panel
  var render = function() {

    // Define right panel
    rightPanel = $('<div/>')
      .attr('id', 'library-right-panel')
      .addClass('pull-right')
      .addClass('col-xs-4')
      .appendTo(tasksPanelParent);

    // Parent container
    var taskInfo = $('<div/>')
      .attr('id', 'library-task-info');

    // Task title
    var taskHeading = $('<h2/>')
      .attr('id', 'library-task-heading')
      .html(task.label)
      .appendTo(taskInfo);

    // Task library name
    var taskLibraryName = $('<h3/>')
      .attr('id', 'library-task-package')
      .html(task.library_name)
      .appendTo(taskInfo);

    // Package author
    var taskAuthor = $('<div/>')
      .attr('id', 'library-task-author')
      .html('<span class="label label-default">Author</span><p>' + task.author + '</p>')
      .appendTo(taskInfo);

    // Task affiliation
    var taskAffiliation = $('<div/>')
      .attr('id', 'library-task-affiliation')
      .html('<span class="label label-default">Affiliation</span><p>' + task.affiliation + '</p>')
      .appendTo(taskInfo);

    // Task description
    var taskDescription = $('<div/>')
      .attr('id', 'library-task-description')
      .html(task.description)
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
      .attr('id', 'library-select-btn')
      .addClass('btn')
      .addClass('btn-default')
      .addClass('btn-primary')
      .attr('data-dismiss', 'modal')
      .html('Select')
      .on('click', function(event) {
        event.preventDefault();
        toSimpleXCell(null,
          Jupyter.notebook.get_selected_index(),
          simplexTaskData[selectedIndex]);
      })
      .appendTo(modalButtons);

    taskInfo.appendTo(rightPanel);
    modalButtons.appendTo(rightPanel);
  };

  /**
   * Update existing rightPanel with currently selected task
   */
  var update = function() {
    $(rightPanel).find('#library-task-heading').html(task.label);
    $(rightPanel).find('#library-task-package').html(task.library_name);
    $(rightPanel).find('#library-task-author').html(task.author);
    $(rightPanel).find('#library-task-affiliation').html(task.affiliation);
    $(rightPanel).find('#library-task-description').html(task.description);
  }


  // Wait for ajax call to load simplexTaskData JSON strings before rendering description.
  var interval = setInterval(function() {
    // Render when ajax call completes
    if (simplexTaskData.length > 0) {
      clearInterval(interval);

      // Create elements as needed, otherwise simply update values
      if ($('#library-right-panel').length == 0) {
        render();
      } else {
        update();
      }
    }
  }, 50);
}

/**
 * Render a card for a given task JSON string. Also responsible for triggering right panel display.
 * @param {String} task_data stringified JSON for a task
 */
const renderTask = function(task_data) {
  // Load json to memory
  var task = JSON.parse(task_data);

  // Generate a card from given task_data
  var cardParent = $('<div/>')
    .addClass('library-card-wrapper')
    .addClass('col-md-6')
    .addClass('col-xs-12')
    .on('click', function(event) {
      event.preventDefault();
      selectedIndex = $(this).index();
      renderRightPanel();
    })
    // Double click auto selects task
    .on('dblclick', function(event) {
      event.preventDefault();
      $('#library-select-btn').click();
    });

  // Card style and click action
  var card = $('<a/>')
    .addClass('library-card')
    .on('click', function(event) {
      event.preventDefault();
      $('.library-card-selected').removeClass('library-card-selected');
      $(this).addClass('library-card-selected');
    });

  // Label/title of method
  var label = $('<h4/>')
    .addClass('card-label')
    .html(task.label);

  // Function's parent package
  var packageTitle = $('<h5/>')
    .addClass('card-package-title')
    .html(task.library_name);

  // Function description
  var description = $('<p/>')
    .addClass('card-description')
    .html(task.description);

  label.appendTo(card);
  packageTitle.appendTo(card);
  description.appendTo(card);
  card.appendTo(cardParent);
  cardParent.appendTo(leftPanel);

  //  tinysort($(leftPanel).children(), '.library-card .card-label');
}
