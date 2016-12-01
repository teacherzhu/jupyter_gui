// Add shim to support Jupyter 3.x and 4.x
var Jupyter = Jupyter || IPython || {}
Jupyter.notebook = Jupyter.notebook || {};
const STATIC_LIB_PATH = location.origin + Jupyter.contents.base_url + "nbextensions/simplex/static/resources/";

/**
 * Holds all JSON for tasks.
 * @type {Array}
 */
var simplexTaskData = [];
var selectedIndex;
var tasksPanelParent, rightPanel, leftPanel;

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
    body: parent
  });

  // Add styling to parent modal container
  var interval = setInterval(function() {
    if ($('.library-parent').length > 0) {
      var libParent = $('.library-parent');
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
 * Initialize panels inside task dialog.
 */
const initTasksPanel = function() {
  tasksPanelParent = $('<div/>').addClass('library-parent');
  initLeftPanel();
  initRightPanel();
}

/******************** HELPER FUNCTIONS ********************/

/**
 * Create left panel showing list of tasks.
 */
var initLeftPanel = function() {
  // Display tasks elements
  leftPanel = $('<div/>')
    .addClass('library-left-panel')
    .addClass('pull-left')
    .addClass('col-xs-8')
    .appendTo(tasksPanelParent);

  // Load tasks
  loadTasks();
  // Load library data
  // loadDefaultTaskData();
  // loadLocalTaskData();
}

var loadTasks = function() {
  $.ajax({
    url: STATIC_LIB_PATH + "simplex.json",
    dataType: "text",
    success: function(simplexData) {
      var tasksDict = JSON.parse(simplexData);

      // Convert dictionary to stringified list
      simplexTaskData = Object.keys(tasksDict).map(function(key) {
        var task = tasksDict[key];
        task.label = key;
        return JSON.stringify(task);
      });
    }
  });
}

/**
 * Create right panel showing package descriptions.
 */
const initRightPanel = function() {

  // Remove and remake with updated values
  if (rightPanel !== undefined) {
    $('.library-right-panel').remove();
  }

  // Display right panel
  rightPanel = $('<div/>')
    .addClass('library-right-panel')
    .addClass('pull-right')
    .addClass('col-xs-4')
    .appendTo(tasksPanelParent);

  // Parse and display task information
  var task = simplexTaskData[selectedIndex];

  // Parent container
  var taskInfo = $('<div/>')
    .addClass('library-task-info');

  // Task title
  var taskHeading = $('<h2/>')
    .addClass('library-task-heading')
    .html(task.label)
    .appendTo(taskInfo);

  // Task library name
  var taskLibraryName = $('<h3/>')
    .addClass('library-task-package')
    .html(task.library_name)
    .appendTo(taskInfo);

  // Package author
  var taskAuthor = $('<div/>')
    .addClass('library-task-author')
    .html('<span class="label label-default">Author</span><p>' + task.author + '</p>')
    .appendTo(taskInfo);

  // Task affiliation
  var taskAffiliation = $('<div/>')
    .addClass('library-task-affiliation')
    .html('<span class="label label-default">Affiliation</span><p>' + task.affiliation + '</p>')
    .appendTo(taskInfo);

  // Task description
  var taskDescription = $('<div/>')
    .addClass('library-task-description')
    .html(task.description)
    .appendTo(taskInfo);

  // Select/cancel buttons
  var modalButtons = $('<div/>')
    .addClass('library-button-group');
  var cancelButton = $('<button>')
    .addClass('btn')
    .addClass('btn-default')
    .attr('data-dismiss', 'modal')
    .html('Cancel')
    .appendTo(modalButtons);
  var selectButton = $('<button>')
    .addClass('btn')
    .addClass('btn-default')
    .addClass('btn-primary')
    .attr('id', 'library-select-button')
    .addClass('disabled')
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
}

/**
 * Load default package tasks from extension static directory.
 */
// const loadDefaultTaskData = function() {
//   console.log('calling loadDefaultTaskData()');
//   $.ajax({
//     url: STATIC_LIB_PATH + "library_list.txt",
//     dataType: "text",
//     success: function(data) {
//       // Load all simplex json files
//       var lib_files = $.trim(data).split('\n');
//
//       // Async request each file
//       for (var i in lib_files) {
//         $.ajax({
//           url: STATIC_LIB_PATH + lib_files[i],
//           dataType: "text",
//           success: function(simplex_data) {
//             addToTasks(simplex_data);
//           },
//           error: function(result) {
//             console.log(STATIC_LIB_PATH + lib_files[i]);
//             console.log('Unable to retrieve library simplex file, ' + lib_files[i] + '.');
//           }
//         });
//       }
//     },
//     // Unable to load library_list.txt file
//     error: function(result) {
//       console.log('library_list.txt file is missing.');
//     }
//   });
// }

// // Load local package tasks from $HOME via Jupyter notebook kernel.
// const loadLocalTaskData = function() {
//   console.log('calling loadLocalTaskData()');
//   var code_input = `
// home_prefix = os.environ['HOME']+'/simplex_data/'
// json_files = os.listdir(home_prefix)
// json_files = [home_prefix + '{}/{}.json'.format(d,d) for d in json_files]
//
// json_str_data = []
// for file in json_files:
//     try:
//         with open(file) as json_file:
//             json_str_data.append(json_file.read())
//     except FileNotFoundError:
//         print('Package JSON file not specified.')
//
// javascript = 'element.append("{}");'.format(json_str_data)
// Javascript(javascript)
// `;
//
//   /**
//    * Import JSON from $HOME using python and export back to javascript.
//    * @param  {[type]} output [description]
//    * @return {[type]}        [description]
//    */
//   var handle_output = function(out) {
//     var result = null;
//     var res;
//     // if output is a print statement
//     if (out.msg_type == "stream") {
//       res = out.content.data;
//     }
//     // if output is a python object
//     else if (out.msg_type === "execute_result") {
//       res = out.content.data["text/plain"];
//     }
//     // if output is a python error
//     else if (out.msg_type == "pyerr") {
//       res = out.content.ename + ": " + out.content.evalue;
//     }
//     // if output is something we haven't thought of
//     else {
//       res = "[out type not implemented]\n" + out;
//     }
//
//     // TODO: Store task json
//     console.log(res);
//   }
//
//   var callbacks = {
//     'iopub': {
//       'output': handle_output
//     }
//   };
//
//   Jupyter.notebook.kernel.execute(code_input, callbacks);
// }


/**
 * Given a package JSON file, generate and display each task specified for the package.
 * @param {String} simplex_data Stringified JSON for a package.
 */
const addToTasks = function(simplex_data) {
  // Load json to memory
  var j = JSON.parse(simplex_data);
  var tasks = j.tasks;
  var path = j.library_path;

  // Generate a card for every task
  for (var index in tasks) {
    var task_data = Object();
    task_data = tasks[index];
    task_data.library_path = j.library_path;
    simplexTaskData.push(JSON.stringify(task_data));

    var cardParent = $('<div/>')
      .addClass('library-card-wrapper')
      .addClass('col-md-6')
      .addClass('col-xs-12')
      .on('click', function(event) {
        event.preventDefault();
        selectedIndex = $(this).index();
        initRightPanel();
      });

    // Card style and click action
    var card = $('<a/>')
      .addClass('library-card')
      .on('click', function(event) {
        event.preventDefault();
        $('.library-card-selected')
          .removeClass('library-card-selected');
        $(this)
          .addClass('library-card-selected');
        $('#library-select-button')
          .removeClass('disabled');
      });

    // Label/title of method
    var label = $('<h4/>')
      .addClass('card-label')
      .html(task_data.label);

    // Function's parent package
    var packageTitle = $('<small/>')
      .addClass('card-package-title')
      .html(task_data.library_name)
      .appendTo(label);

    // Function description
    var description = $('<p/>')
      .addClass('card-description')
      .html(task_data.description);

    label.appendTo(card);
    description.appendTo(card);
    card.appendTo(cardParent);
    cardParent.appendTo(leftPanel);
  }
}
