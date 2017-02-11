// Add shim to support Jupyter 3.x and 4.x
var Jupyter = Jupyter || IPython || {}
Jupyter.notebook = Jupyter.notebook || {};
var fieldGroups = ['required_args', 'optional_args', 'returns'];
var groupLabels = ['Input', 'Optional Input', 'Output'];

// TODO WIDGET STYLING VARIABLES
var widgetFont;
var inputColor;
var optInputColor;
var outputColor;

/**
 * Gets the taskJSON from the given cell following the Simpli Widget format.
 * @param  {Object} cell Simpli cell
 * @return {Object}      Returns the widget's associated JSON object
 */
var getWidgetData = function(cell) {
  // Scrape JSON from cell
  var taskJSON = cell.get_text().split('\n').slice(-1)[0];
  taskJSON = taskJSON.slice(4, taskJSON.length - 3);
  taskJSON = JSON.parse(taskJSON);
  return taskJSON;
}

/**
 * Renders Task Widget and attaches interactive capabilities.
 * @param  {number} cellIndex  Index of the cell that the task widget will be attached to
 * @param  {Object} taskJSON   JSON object for task
 * @return {str}               String representation of widget HTML
 */
var renderTaskWidget = function(cellIndex, taskJSON) {
  var cell = Jupyter.notebook.get_cell(cellIndex);

  // Scrape JSON from cell
  if (taskJSON == undefined) {
    taskJSON = getWidgetData(cell);
  }

  // Generate Widget HTML and display by executing %%HTML cell.
  updateTaskWidget(cell, taskJSON);
  cell.widgetarea._clear();
  cell.execute();
  cell.expand_output();

  // Setup widget interactions after it renders
  var setupInteractions = setInterval(function() {
      if (!Jupyter.notebook.kernel_busy) {
        clearInterval(setupInteractions);

        $('.item-header').each(function(index, element) {

          // Show all panels except optional args
          if (!$(element).parent().hasClass('field-optional_args-group') &&
            !$(element).parent().hasClass('field-group-content')) {
            $(element).next().show();
          }

          $(element).click(function() {
            $(element).next().toggle();
          })
        });

        // Save user input from form in %%HTML
        var saveUserInput = function() {
          var form = cell.element.find('form')[0];
          var userInput = form.serialize();

          for (var group of fieldGroups) {

            // Convert single element to array, ignore if empty
            if (!(userInput[group] instanceof Array) && userInput[group] != undefined) {
              userInput[group] = [userInput[group]];
            }

            // Map user input values to argument JSON
            for (var inputIndex in userInput[group]) {
              var inputValue = userInput[group][inputIndex];
              inputValue = inputValue.split('"').join('').split("'").join('');
              taskJSON[Object.keys(taskJSON)[0]][group][inputIndex].value = inputValue;
            }
          }

          // Save user input to widget HTML
          updateTaskWidget(cell, taskJSON);
        };

        // Update widget code whenever user types
        $('paper-input').keyup(function(e) {
          setTimeout(function() {
            saveUserInput();
          }, 50);

        });

        // Link submitting form to executing function
        cell.element.find('form').on('iron-form-submit', function(event) {
          if (this.validate()) {

            // Compile task JSON
            var pythonTask = JSON.stringify(taskJSON);
            var taskCode =
              `# ${AUTO_OUT_FLAG}\nmgr.execute_task('''${pythonTask}''')\nsync_manager_to_notebook()`;

            // Append output to Widget cell
            var outputCallback = function(msg) {
              // Clear output except for widget
              cell.output_area.handle_output(msg);
            }

            var interval = setInterval(function() {
              // Use kernel to read library JSONs
              if (!Jupyter.notebook.kernel_busy) {
                clearInterval(interval);
                var output_area = cell.output_area;
                // Delete output displayed after Widget
                if (output_area.element && output_area.element[0].children.length > 1) {
                  output_area.element[0].removeChild(output_area.element[0].children[1]);
                  output_area.outputs.pop();
                }
                Jupyter.notebook.kernel.execute(taskCode, {
                  'iopub': {
                    'output': outputCallback
                  }
                });
              }
            }, 10);
          }
        });
      }
    },
    50);
}

/**
 * Updates task widget HTML with user input values.
 * @param  {object} cell     The cell that the task widget is attached to
 * @param  {object} taskJSON task JSON object
 */
var updateTaskWidget = function(cell, taskJSON) {
  var updatedHTML = generateTaskWidgetHTML(taskJSON);
  cell.set_text(updatedHTML + `\n<!--${JSON.stringify(taskJSON)}-->`);
}

/**
 * Generates HTML for a task widget that is executed via HTML magic with the python kernel.
 * @param  {Object} taskJSON JSON object for task
 * @return {str}             String representation of widget HTML
 */
var generateTaskWidgetHTML = function(taskJSON) {
  var label = Object.keys(taskJSON)[0];
  var taskData = taskJSON[label];

  var widget = $('<paper-material>')
    .addClass('task-widget')
    .attr('elevation', '1');

  var widgetHeader = $('<div>')
    .addClass('task-widget-header')
    .addClass('item-header')
    .html(`<h2>${label}</h2>`)
    .appendTo(widget);

  // Outer container
  var widgetContentOuter = $('<iron-collapse>')
    .addClass('task-widget-inner')
    .appendTo(widget);

  // Inner content
  var widgetContent = $('<div>')
    .addClass('task-widget-content')
    .addClass('item-content')
    .appendTo(widgetContentOuter);

  var taskInfo = $('<div>')
    .addClass('widget-info')
    .html(taskData.description)
    .appendTo(widgetContent);

  var widgetForm = $('<form>')
    .attr({
      is: 'iron-form',
      class: 'task-widget-form'
    })
    .appendTo(widgetContent);

  // Form panel for user entry
  var formPanel = $('<div>')
    .addClass('widget-form-panel')
    .appendTo(widgetForm);

  // Generate fieldGroups of arguments
  for (var groupIndex in fieldGroups) {
    // Generate group only if listed in config
    var g = taskData[fieldGroups[groupIndex]];
    if (g.length > 0) {

      // Input group container
      var fieldGroup = $('<div>')
        .addClass('field-group')
        .addClass('field-' + fieldGroups[groupIndex] + '-group')
        .appendTo(formPanel);

      var fieldGroupHeader = $('<div>')
        .addClass('item-header')
        .html(
          `<h3>${groupLabels[groupIndex]}</h3>
               <paper-icon-button icon="info"></paper-icon-button`)
        .appendTo(fieldGroup);


      // Contents = many fields
      var fieldGroupContent = $('<iron-collapse>')
        .appendTo(fieldGroup);

      var fieldGroupContentInner = $('<div>')
        .addClass('field-group-content')
        .addClass('item-content')
        .appendTo(fieldGroupContent);

      for (var argIndex in g) {
        var arg = g[argIndex];

        // TODO toggle itemContent on click
        var itemHeader = $('<div>')
          .addClass('item-header')
          .appendTo(fieldGroupContentInner);

        // Generate a field for each argument
        var field = $('<paper-input>')
          .attr({
            label: arg.label,
            name: fieldGroups[groupIndex],
            value: arg.value
          })
          .appendTo(itemHeader);

        if (fieldGroups[groupIndex] != 'optional_args') {
          field.attr({
            'auto-validate': '',
            'error-message': 'Required!',
            required: ''
          });
        }

        // Generate info text for each argument field
        var itemContentCollapse = $('<iron-collapse>')
          .appendTo(fieldGroupContentInner);

        var itemContent = $('<div>')
          .addClass('item-content')
          .html(`${arg.description}`)
          .appendTo(itemContentCollapse);

      }
    }
  }
  // Create button that submits iron form
  var submitButtonWrapper = $('<button>')
    .addClass('form-submit-button-wrapper')
    .appendTo(widgetForm);
  var submitButton = $('<paper-button>')
    .addClass('form-submit-button')
    .attr('raised', '')
    .html('submit')
    .appendTo(submitButtonWrapper);

  // Create icon for submit button
  var submitIcon = $('<iron-icon>')
    .attr('icon', 'assessment')
    .appendTo(submitButton);

  // Return raw html for widget
  return `%%HTML\n<!--${AUTO_EXEC_FLAG}-->\n` + widget.prop('outerHTML');
}

/**
 * [setItemInfo description]
 * @param {[type]} index [description]
 * @param {[type]} cell  [description]
 */
// var setItemInfo = function(index, cell) {
//   var items = cell.element.find('.item-info');
//   items.hide(0);
//   $(items[index]).fadeIn('fast');
// }
