from flask import Flask
from flask_ac import ACManager, permissions_required

p = {
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


app = Flask(__name__)
ac_manager = ACManager(p)
ac_manager.init_app(app)


def callback():
    return 'failed', 1


@app.before_request
def inject_user():
    from flask import g
    g.user = {
        'uid': 'uid-123',
        'roles': [
            {
                'name': 'admin',
                'permissions': ['P0-3', 'P0-2-1', 'P0-2-2']
            },
        ]
    }


@app.route('/test')
@permissions_required(permissions=['P0-2-2'], failed_callback=callback)
def test():
    return 'success', 1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
