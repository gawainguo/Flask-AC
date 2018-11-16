# Flask-AC

Flask-AC is a light-weighted access control extension for Flask. It implement role based access control(rbac) by permissions tree data structure which modeling permissions in tree-like hierarchy.

Flask-AC will not handling the storage of roles and permissions. Instead, by providing the loader for permissions and roles, you can customize how the data stored in database or context.

## Installation

Install the extension with pip:
```
pip install flask-ac
```

## Usage
Like other extensions, flask-ac provide init_app and ACManager class to initialize the extension.

To create a instance of ACManager, passing the permissions structure dict object to the constructor(we will introduce this object later):
```
import flask_ac

ac_manager = flask_ac.ACManager(permissions)
```

And use init_app to bound the current Flask app:
```
import flask

app = flask.Flask(__name__)
ac_manager.init_app(app)
```

Once initialized, you can use roles_required and permissions_required decorators in your view function or any funcions:

```
from flask_ac import permissions_required

@app.route('/test')
@permissions_required(permissions=['edit-user-profile'], failed_callback=callback)
def test():
    return 'success', 200
```

This shows the basic usage of flask-ac, which use default loaders for roles and permissions. We will discuss the details of other use cases.

## Concepts

### Permission
A permission has key and name attributes. Also there is a list of child permisisons called children which represent sub-permissions under current permission. This structure is what we called permission tree(ptree). 

To use flask-ac, you need to specify your permission hierarchy to ACManager. Currently it only support dict object. Here is a example of permissions:
```
permissions = {
    name: 'Super Administrator Permission',
    key: 'super-admin',
    children: [
        {
            name: 'Customer Service Admin Permission',
            key: 'customer-service-admin',
            children: [
                {
                    name: 'Customer Service Edit Permission',
                    key: 'customer-service-edit
                },
                {
                    name: 'Customer Service View Permission',
                    key: 'customer-service-view
                },
            ]
        },
        {
            name: 'Data Service Admin Permission',
            key: 'data-service-admin',
            children: [
                {
                    name: 'Data Service Edit Permission',
                    key: 'data-service-edit
                },
                {
                    name: 'Data Service View Permission',
                    key: 'data-service-view
                },
            ]
        }
    ]
}
```
In above example, we defined 3 levels of permissions. If an api has a permission required 'data-service-edit', the user who has one of ['super-admin', 'data-service-admin', ''data-service-edit'] permissions will successfully access the resource. Otherwise it will failed.

Currently, flask-ac only support a single root permission.

In database, flask-ac recommend only store the key in user/role table instead of whole hierachy, and store the ptree separately.

### Role
A role is a group of permissions, which can provide permissiosn to users easily. Role is just a flat list data structure, which is different from ptree. And when you want to control the access by role, flask-ac is simply check if the user has the specific role.

### Loaders
As said before, flask-ac will not provide any storage for role/permissions, so you need to write loaders to load the permissions of current user from context.

In default, flask-ac will load the user from flask global 'g' with following structure:

```
from flask import g

g.user = {
    roles: [
        'name': 'admin',
        'permissions': [
            'super-admin'
        ]
    ]
}
```

If you user is store in session, you can write your own loaders and pass it to ac_manager when initializing:
```
from flask import session, Flask
from flask_ac import ACManager

def roles_loader():
    user = session['user']
    roles = user.get('roles', [])
    return [role['name'] for role in roles]

def permissions_loader():
    user = session['user']
    permissions = user['permissions']
    return permissions

app = Flask(__name__)
permissions = get_permissions()

ac_mamager = ACManager(permissions,
    roles_loader=roles_loader, permissions_loader=permissions_loader)
ac_manager.init_app(app)
```

[![Analytics](https://ga-beacon.appspot.com/UA-129310551-2/index)](https://github.com/gawainguo/Flask-AC)