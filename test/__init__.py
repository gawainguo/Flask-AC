from flask import Flask

test_permission = {
    'name': 'root',
    'key': 'P0',
    'children': [
        {
            'name': 'p0-1',
            'key': 'P0-1',
            'children': [
                {
                    'name': 'P0-1-1',
                    'key': 'P0-1-2',
                },
                {
                    'name': 'P0-1-2',
                    'key': 'P0-1-2',
                },
            ]
        },
        {
            'name': 'p0-2',
            'key': 'P0-2',
            'children': [
                {
                    'name': 'P0-2-1',
                    'key': 'P0-2-1',
                },
                {
                    'name': 'P0-2-2',
                    'key': 'P0-2-2',
                },
            ]
        },
        {
            'name': 'p0-3',
            'key': 'P0-3',
            'children': [
            ]
        }
    ]
}


test_app = Flask(__name__)
