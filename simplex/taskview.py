from ipywidgets import widgets as w
from functools import partial


class TaskView:
    """
    Viewing class for Task.
    """

    def __init__(self, task_manager, task):
        """
        Constructor.
        :param task_manager: TaskManager;
        :param task: Task;
        """

        self.task_manager = task_manager
        self.task = task

        self.fields = {'input': {}, 'optional_input': {}, 'output': []}

        # TODO: think of calling without partial
        # Hook for running the task

    # TODO: test
    def callback(self, unused_widget_item):
        self.task_manager.submit(self.fields, self.task)

    def create(self):
        """
        Make the whole widget panel, containing input, optional input, and output fields.
        :return: Box;
        """

        panel = w.Box().add_class('panel').add_class('panel-default').add_class('my-panel')
        panel.children = tuple([self.heading(), self.body()])
        return panel

    def heading(self):
        """
        Make task heading.
        :return: Box;
        """

        heading = w.Box().add_class('panel-heading')
        text = w.HTML('<h1>' + self.task.label + '</h1>')
        heading.children = tuple([text])
        return heading

    def body(self):
        """
        Make task body, consisting of input, optional input, and output boxes.
        :return: Box;
        """
        # TODO: modularize field making

        # Make parent box
        body = w.Box().add_class('panel-body')

        # Make required input box(s)
        input_elements = [w.HTML('<h3>Input Parameters<h3/>')]
        input_elements.extend([self.text_field(arg['label'],
                                               arg['description'],
                                               'input',
                                               input_name=arg['arg_name'])
                               for arg in self.task.required_args])

        # Make optional input box(s)
        opt_input_elements = [w.HTML('<h3>Optional Input<h3/>')]
        opt_input_elements.extend([self.text_field(arg['label'],
                                                   arg['description'],
                                                   'optional_input',
                                                   input_name=arg['arg_name'])
                                   for arg in self.task.optional_args])

        # Make output box(s)
        output_elements = [w.HTML('<h3>Output<h3/>')]
        output_elements.extend([self.text_field(arg['label'],
                                                arg['description'],
                                                'output')
                                for arg in self.task.return_names])

        # Make execute_task box
        run_button = w.Button(description="RUN")
        run_button.add_class('btn').add_class(
            'btn-primary').add_class('execute_task-btn')
        run_button.on_click(self.callback)

        # add to body
        all_elements = []

        if len(input_elements) > 1:
            all_elements.extend(input_elements)
        if len(opt_input_elements) > 1:
            all_elements.extend(opt_input_elements)
        if len(output_elements) > 1:
            all_elements.extend(output_elements)
        all_elements.append(run_button)
        body.children = tuple(all_elements)

        return body

    def text_field(self, label, description, field_type, input_name=None):
        """
        Make a box.
        :param label: str; label
        :param description: str; description
        :param field_type: str; box type
        :param input_name: dictionary key if box_type is required input or optional input
        :return: Box; parent
        """

        # Make box
        field = w.Text(description=label).add_class('form-group')

        # Hook the box with the callback
        field.on_submit(self.callback)

        # Make help button
        help_button = w.Button(description='?', tooltip=description)

        # Make parent box and have it host the box
        parent = w.Box().add_class('my-text-field')
        parent.children = tuple([field, help_button])

        # Update fields
        if input_name:
            self.fields[field_type][input_name] = field
        else:
            self.fields[field_type].append(field)

        return parent
