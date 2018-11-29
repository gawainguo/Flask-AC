from flask_ac import ACManager
from . import test_permission, test_app


def test_init_app():
    ac = ACManager(permissions=test_permission)
    ac.init_app(test_app)
    assert test_app.ac_manager.ptree.name == test_permission.get('name')
