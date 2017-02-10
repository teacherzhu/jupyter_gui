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

  // Setup widget interactions after it renders
  var setupInteractions = setInterval(function() {
      if (!Jupyter.notebook.kernel_busy) {
        clearInterval(setupInteractions);

        // Left panel sets max widget height
        $('.widget-panel-right').css('height', $('.widget-panel-left').css('height'));
        $('.widget-panel-right').css('max-height', $('.widget-panel-left').css('height'));

        // Bind and show corresponding description on focus
        var itemInputs = cell.element.find("paper-input");
        itemInputs.each(function(index) {
          $(this).on('focus', function() {
            setItemInfo(index, cell);
          });
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
              `# ${AUTO_OUT_FLAG}\nmgr.execute_task(json.loads('''${pythonTask}'''))\nsync_manager_to_notebook()`;

            // var outputCell;
            // // Create output cell if not created already
            // if (!Jupyter.notebook.get_cell(cellIndex + 1)) {
            //   Jupyter.notebook.insert_cell_below();
            // }
            //
            // Jupyter.notebook.select_next();
            // outputCell = Jupyter.notebook.get_selected_cell();
            //
            // // Don't touch cell if not output cell and make cell directly below widget cell
            // var cellContent = outputCell.get_text().trim();
            // if (cellContent !== "" && cellContent.indexOf(AUTO_OUT_FLAG) < 0) {
            //   Jupyter.notebook.insert_cell_above();
            //   Jupyter.notebook.select_prev();
            //   outputCell = Jupyter.notebook.get_selected_cell();
            // }
            //
            // // Execute task
            // outputCell.set_text(taskCode);
            // outputCell.execute();

            // Append output to Widget cell
            var outputCallback = function(msg) {
              // Clear output except for widget
              // var output = cell.output_area.outputs[0];
              // cell.output_area.handle_output(output);
              // console.log('POST-EXECUTE');
              console.log(msg);
              // var outputJSON = out.content;
              // outputJSON.output_type = out.msg_type;
              cell.output_area.handle_output(msg);
            }

            var interval = setInterval(function() {
              // Use kernel to read library JSONs
              if (!Jupyter.notebook.kernel_busy) {
                clearInterval(interval);
                var output_area = cell.output_area;
                // TODO fix me
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
  // Outer container
  var widget = $('<paper-material>')
    .attr({
      elevation: '2',
      class: 'task-widget'
    });

  // Inner content
  var widgetInner = $('<paper-collapse-item>')
    .addClass('task-widget-inner')
    .attr({
      header: `<h1>${label}</h1>`,
      opened: 'True'
    })
    .appendTo(widget);

  // Left side panel for form
  var leftPanel = $('<div>')
    .addClass('widget-panel')
    .addClass('widget-panel-left')
    .appendTo(widgetInner);

  var widgetForm = $('<form>')
    .attr({
      is: 'iron-form',
      class: 'task-widget-form'
    })
    .appendTo(leftPanel);

  // Generate fieldGroups of arguments
  for (var groupIndex in fieldGroups) {
    // Generate group only if listed in config
    var g = taskData[fieldGroups[groupIndex]];
    if (g.length > 0) {
      var groupWrapper = $('<div>')
        .addClass('form-group-wrapper')
        .appendTo(widgetForm);

      // Input container
      var fieldGroup = $('<paper-collapse-item>')
        .addClass('field-group')
        .addClass('field-' + fieldGroups[groupIndex] + '-group')
        .attr('header', groupLabels[groupIndex])
        .appendTo(groupWrapper);

      // Default show/hide setting
      if (fieldGroups[groupIndex] != 'optional_args') {
        fieldGroup.attr('opened', 'True');
      }

      // Generate a field for each argument
      for (var argIndex in g) {
        var arg = g[argIndex];
        var field = $('<paper-input>')
          .attr({
            label: arg.label,
            name: fieldGroups[groupIndex],
            required: '',
            value: arg.value
          });

        if (fieldGroups[groupIndex] != 'optional_args') {
          field.attr({
            'auto-validate': '',
            'error-message': 'Required!'
          });
        }
        field.appendTo(fieldGroup);
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
    .html('run')
    .appendTo(submitButtonWrapper);

  // Create icon for submit button
  var submitIcon = $('<iron-icon>')
    .attr('icon', 'done')
    .appendTo(submitButton);

  // Right side panel for description
  var rightPanel = $('<div>')
    .addClass('widget-panel')
    .addClass('widget-panel-right')
    .appendTo(widgetInner);

  // Shown
  var taskInfo = $('<div>')
    .addClass('task-info')
    .html(taskData.description)
    .appendTo(rightPanel);

  for (var groupIndex in fieldGroups) {
    // Generate group only if listed in config
    var g = taskData[fieldGroups[groupIndex]];
    if (g.length > 0) {
      // Extract description for each parameter
      for (var arg of g) {
        var itemInfo = $('<li>')
          .addClass('item-info')
          .html(`<h3>${arg.label}</h3><p>${arg.description}</p>`)
          .hide()
          .appendTo(rightPanel);
      }
    }
  }


  // Return raw html for widget
  return `%%HTML\n<!--${AUTO_EXEC_FLAG}-->\n` + widget.prop('outerHTML');
}

/**
 * [setItemInfo description]
 * @param {[type]} index [description]
 * @param {[type]} cell  [description]
 */
var setItemInfo = function(index, cell) {
  var items = cell.element.find('.item-info');
  items.hide(0);
  $(items[index]).fadeIn('fast');
}
