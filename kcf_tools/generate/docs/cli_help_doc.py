from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError


class CompNameValidator(Validator):
    COMPONENT_TYPES = [" ex", " wr", "app", " extractor", " writer", "application"]

    def validate(self, document):
        for type_str in self.COMPONENT_TYPES:
            if type_str in document.text.lower():
                raise ValidationError(
                    message='Please do not have the component type in the name',
                    cursor_position=len(document.text))


def cli_questions():
    print('Generate Help Documentation')
    questions = [
        {
            'type': 'input',
            'name': 'component_name',
            'message': 'What is the title of the Component (without component type)',
            'validate': CompNameValidator,
        },
        {
            'type': 'list',
            'name': 'component_type',
            'message': 'What type of component is it?',
            'choices': ['Extractor', 'Writer', 'Application'],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'list',
            'name': 'component_type_category',
            'message': 'What type of Extractor is it?',
            'choices': ['communication', 'database', 'marketing-sales', 'social', 'storage', 'other'],
            'when': lambda answers: answers['component_type'] == 'extractor'
        },
        {
            'type': 'list',
            'name': 'component_type_category',
            'message': 'What type of Writer is it?',
            'choices': ['bi-tools', 'database', 'marketing-sales', 'storage', 'other'],
            'when': lambda answers: answers['component_type'] == 'writer'
        },
        {
            'type': 'list',
            'name': 'component_type_category',
            'message': 'What type of Application is it?',
            'choices': ['triggers', 'other'],
            'when': lambda answers: answers['component_type'] == 'application'
        }
    ]

    answers = prompt(questions)
    return answers
