# How to configure Django-Doorkeeper

## Required Steps

### Install middleware

```python
# my_project/settings.py
MIDDLEWARE = [
    # Doorkeeper should be the very first middleware in the list
    'doorkeeper.middleware.DoorkeeperMiddleware',
    # ...
]
```

### Configure required settings

```python
# my_project/settings.py
DOORKEEPER = {
    'PASSWORD': 'open sesame', # The password to enter the site, shared by all users.  Choose your own password, and don't use "open sesame", please.
    'ENABLED': True,
    'DEFAULT_REDIRECT_URL': reverse_lazy('home'), # The URL to redirect to after entering the password.
}
```

When redirecting the user to the password prompt, doorkeeper attempts to keep track of the URL they were trying to access. If the user successfully authenticates, they will be redirected to the URL they were trying to access. If we lose track of the URL or none is provided (as can happen with bookmarks or when sharing links), the user will be redirected to the `DEFAULT_REDIRECT_URL`.

### Add URLPattern for doorkeeper view

```python
# my_project/urls.py
urlpatterns = [
    path('doorkeeper/', include('doorkeeper.urls')),
]
```

## Optional

### Display form for doorkeeper exit view

```html
<!-- my_project/templates/my_app/base_template.html -->

<form method="post" action="{% url 'doorkeeper:exit' %}">
  {% csrf_token %}
  <button type="submit" class="style-as-desired">Exit Site Preview</button>
</form>
```

You may want to place this button in your navigation or hovering in the bottom right corner, etc. Submitting the form will remove the Doorkeeper cookie and cause subsequent requests in the same browser to be redirected to the Doorkeeper password prompt.

### Override password prompt template

The default template is extremely barebones. You can override it by creating a template in your project.

<!-- prettier-ignore-start -->
```html
<!-- my_project/templates/doorkeeper/doorkeeper_entrance.html -->

{% extends "my_app/base_template.html" %}

{% block some_block_name %}

    <form method="post" action="{% url 'doorkeeper:entrance' %}?{{ next_url_param_name }}={{ next_url }}">
        {% csrf_token %} {{ form.as_div }}
        <button type="submit">Enter</button>
    </form>

{% endblock %}
```
<!-- prettier-ignore-end -->

### Optional settings

```python
# my_project/settings.py
DOORKEEPER = {
    'BYPASS_PATHS': [ '/some-public-path/',  reverse_lazy('other-public-path'), ...], # List of paths that bypass Doorkeeper and do not require the password to have been entered before accessing them.  If not provided, defaults to ['/favicon.ico',]
    'COOKIE_AGE': 60 * 60 * 24 * 7 * 2,  # defaults to the value of SESSION_COOKIE_AGE, which defaults to 2 weeks
    'COOKIE_DOMAIN': None,  # if not provided, defaults to the value of SESSION_COOKIE_DOMAIN, which defaults to None, which uses the standard domain cookie
    'COOKIE_EXPIRE_AT_BROWSER_CLOSE': False,  # if not provided, defaults to the value of SESSION_EXPIRE_AT_BROWSER_CLOSE, which defaults to False
    'COOKIE_HTTPONLY': True|False,  # if not provided, defaults to the value of SESSION_COOKIE_HTTPONLY, which defaults to True
    'COOKIE_NAME': 'my_cookie_name', # if not provided, defaults to 'doorkeeper_cookie'
    'COOKIE_PATH': '/app-root/', # if not provided, defaults to the value of SESSION_COOKIE_PATH, which defaults to '/'.  Use this if your Django app is not installed at the root of your domain.
    'COOKIE_SAMESITE': 'Lax'|'Strict'|'None',  # if not provided, defaults to the value of SESSION_COOKIE_SAMESITE, which defaults to 'Lax'
    'COOKIE_SECURE': True|False,  # if not provided, defaults to the value of SESSION_COOKIE_SECURE, which defaults to False
    'EXIT_REDIRECT_URL': reverse_lazy('bypassed-home'), # The URL to redirect to after exiting the site.  Defaults to the Doorkeeper password prompt view
    'NEXT_URL_PARAM_NAME': 'some_param_name', # Name of the URL query parameter used to store redirect URLs. if not provided, defaults to 'doorkeeper_next_url'
    'REDIRECT_ALLOWED_HOSTS': ['example.com', 'localhost', '127.0.0.1'], # List of hosts to always allow redirecting to upon success. If not provided, defaults to an empty set.  The current hostname of a given request is always treated as allowed even if not in this list.  If you put untrusted hostnames in here, that could introduce security issues such as phishing vulnerabilities.
}
```

### Exempt Views from Doorkeeper

Instead of (or in addition to) using the `BYPASS_PATHS` setting, you can wrap the views you want to exempt from Doorkeeper with the `doorkeeper_exempt` decorator.

```python
# my_app/urls.py

from doorkeeper.decorators import doorkeeper_exempt

urlpatterns = [
    # ...
    path('some-public-path/', doorkeeper_exempt(SomeView.as_view()), name='some-public-path'),
]
```
