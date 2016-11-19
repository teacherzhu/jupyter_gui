// Add shim to support Jupyter 3.x and 4.x
var Jupyter = Jupyter || IPython || {};
Jupyter.notebook = Jupyter.notebook || {};
var STATIC_LIB_PATH = location.origin + Jupyter.contents.base_url + "nbextensions/simplex/simplex_library/";
var simplexLibrary = [];
var parent, rightPanel, leftPanel;

/******************** MAIN FUNCTIONS ********************/
var showLibraryPanel = function() {
    var dialog = require('base/js/dialog');
    initLibraryPanel();

    dialog.modal({
        notebook: Jupyter.notebook,
        keyboard_manager: Jupyter.notebook.keyboard_manager,
        body: parent
    });

    // add styling to parent modal container
    var interval = setInterval(function() {
        if ($('.library-parent').length > 0) {
            $('.library-parent').parent()
                .addClass('library-modal-body');
            $('.library-parent').parents('.modal-content')
                .find('.modal-header')
                .addClass('library-modal-header');
            $('.library-parent').parents('.modal-content')
                .find('.modal-footer')
                .addClass('library-modal-footer');
            $('.library-parent').parents('.modal-dialog')
                .addClass('library-modal-dialog');
            clearInterval(interval);
        }
    }, 100);

}

var initLibraryPanel = function() {
    parent = $('<div/>')
        .addClass('library-parent');

    initRightPanel();
    initLeftPanel();

    load_libraries();
}

/******************** HELPER FUNCTIONS ********************/

var initRightPanel = function() {
    // Display right panel
    rightPanel = $('<div/>')
        .addClass('library-right-panel')
        .addClass('pull-right')
        .addClass('col-xs-4')
        .appendTo(parent);

    // Task information
    var taskInfo = $('<div/>')
        .addClass('library-task-info');
    var taskHeading = $('<h2/>')
        .addClass('library-task-heading')
        .appendTo(taskInfo)
        .html('Define Components <small>CCAL</small>');
    var taskAuthor = $('<div/>')
        .addClass('library-task-author')
        .appendTo(taskInfo)
        .html('<span class="label label-default">Author</span><p>Huwate Yeerna</p>');
    var taskAffiliation = $('<div/>')
        .addClass('library-task-affiliation')
        .appendTo(taskInfo)
        .html('<span class="label label-default">Affiliation</span><p>Moores Cancer Center</p>');
    var taskAffiliation = $('<div/>')
        .addClass('library-task-affiliation')
        .appendTo(taskInfo)
        .html('<span class="label label-default">Site</span><p>Moores Cancer Center</p>');
    var taskDescription = $('<div/>')
        .addClass('library-task-description')
        .appendTo(taskInfo)
        .html('Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dolores, qui accusamus vero libero mollitia et harum, assumenda dolore sequi reprehenderit voluptatum in amet pariatur, unde provident nostrum dolorem dolorum maiores.');

    // select/cancel buttons
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
        .attr('data-dismiss', 'modal')
        .html('Select')
        .appendTo(modalButtons);

    taskInfo.appendTo(rightPanel);
    modalButtons.appendTo(rightPanel);
}

var initLeftPanel = function() {
    // Display library elements
    leftPanel = $('<div/>')
        .addClass('library-left-panel')
        .addClass('pull-left')
        .addClass('col-xs-8')
        .appendTo(parent);
}

// read in file listing
var load_libraries = function() {
    $.ajax({
        url: STATIC_LIB_PATH + "library_list.txt",
        dataType: "text",
        success: function(data) {

            var lib_files = $.trim(data).split('\n');
            // load all simplex json files
            for (var i in lib_files) {

                // try to load each file
                $.ajax({
                    url: STATIC_LIB_PATH + lib_files[i],
                    dataType: "text",
                    success: function(simplex_data) {
                        addToLibrary(simplex_data);
                    },
                    error: function(result) {
                        console.log(STATIC_LIB_PATH + lib_files[i]);
                        console.log('Unable to retrieve library simplex file, ' + lib_files[i] + '.');
                    }
                });
            }
        }
    });
}

var addToLibrary = function(simplex_data) {
    simplexLibrary.push(simplex_data);
    var j = JSON.parse(simplex_data);
    var tasks = j.tasks;
    var path = j.library_path;
    var package_title;
    if (path.split('/')[path.split('/').length - 1] == "") {
        package_title = path.split('/')[path.split('/').length - 2];
    } else {
        package_title = path.split('/')[path.split('/').length - 1];
    }

    for (var index in tasks) {
        // Generate card
        var cardParent = $('<div/>')
            .addClass('library-card-wrapper')
            .addClass('col-md-4')
            .addClass('col-sm-6')
            .addClass('col-xs-12');
        var card = $('<a/>')
            .addClass('library-card');
        var label = $('<h4/>')
            .addClass('card-label')
            .html(tasks[index].label)
            .appendTo(card);
        var packageTitle = $('<p/>')
            .addClass('card-package-title')
            .html(package_title)
            .appendTo(card);
        var description = $('<p/>')
            .addClass('card-description')
            .html(tasks[index].description)
            .appendTo(card);
        card.appendTo(cardParent);
    }
    cardParent.appendTo(leftPanel);
}
