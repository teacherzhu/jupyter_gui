from ipywidgets import widgets as w


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

    # TODO: test
    def callback(self, unused_widget_item):
        self.task_manager.submit(self.fields, self.task)

    def create(self):
        """
        Make the whole widget panel, containing input, optional input, and output fields.
        :return: Box; parent container
        """

        form_panel = w.Box().add_class('form-panel')
        form_panel.children = tuple([self.heading(), self.body()])
        # Outer div to contain both the js-widget element as well as
        # js-generated elements.
        wrapper = w.Box().add_class('panel-wrapper')
        wrapper.children = tuple([form_panel])
        return wrapper

    def heading(self):
        """
        Make task heading.
        :return: Box; parent container
        """

        heading = w.Box().add_class('form-panel-heading')
        text = w.HTML('<h1>' + self.task.label + '</h1>')
        heading.children = tuple([text])
        return heading

    def body(self):
        """
        Make task body, consisting of input, optional input, and output boxes.
        :return: Box; parent container
        """

        # Make parent box
        body = w.Box().add_class('form-panel-body')

        # Make required input box(es)
        input_elements = self.field_group(
            'Input', self.task.required_args, 'input')

        # Make optional input box(es)
        opt_input_elements = self.field_group('Optional Input',
                                              self.task.optional_args, 'optional_input')

        # Make output box(es)
        output_elements = self.field_group(
            'Output', self.task.return_names, 'output')

        # Make run button
        run_button = w.Button(description="RUN")
        run_button.add_class('btn').add_class(
            'btn-primary').add_class('run-task-btn')
        run_button.on_click(self.callback)

        # add to body
        field_groups = []

        if len(input_elements.children) > 1:
            field_groups.append(input_elements)
        if len(opt_input_elements.children) > 1:
            field_groups.append(opt_input_elements)
        if len(output_elements.children) > 1:
            field_groups.append(output_elements)
        body_inner = w.Box().add_class('form-panel-body-inner')
        body_inner.children = tuple(field_groups)

        body.children = tuple([body_inner, run_button])

        return body

    def field_group(self, label, field_args, field_type):
        """
        Make an group of fields with the appropriate header and input fields.
        :param label: str; heading text
        :param field_args: list; self.fields list to populate field group with
        :param field_type: str; specifies field group type
        :return: Box; parent container
        """
        input_elements = [w.HTML('<h3>{}<h3/>'.format(label))]

        if field_type == 'output':
            input_elements.extend([self.text_field(arg['label'],
                                                   arg['description'],
                                                   field_type)
                                   for arg in field_args])

        else:
            input_elements.extend([self.text_field(arg['label'],
                                                   arg['description'],
                                                   field_type,
                                                   input_name=arg['arg_name'])
                                   for arg in field_args])

        # FIXME: use class
        parent = w.Box().add_class('form-{}-group'.format(field_type))
        parent.children = tuple(input_elements)
        return parent

    def text_field(self, label, description, field_type, input_name=None):
        """
        Make a box.
        :param label: str; label
        :param description: str; description
        :param field_type: str; box type
        :param input_name: dictionary key if box_type is required input or optional input
        :return: Box; parent container
        """
        # Make box
        field = w.Text(placeholder=label).add_class('form-group')

        # Hook the box with the callback
        field.on_submit(self.callback)

        # Make help button
        help_button = w.Button(description='?', tooltip=description)

        # Make parent box and have it host the box
        parent = w.Box().add_class('form-panel-text-field')
        parent.children = tuple([field, help_button])

        # Update fields
        if input_name:
            self.fields[field_type][input_name] = field
        else:
            self.fields[field_type].append(field)

        return parent
