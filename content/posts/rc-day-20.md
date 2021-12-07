---
title: "Recurse Center Day 20: Django v4 upgrade (from v1)"
date: "2021-12-02T17:18:07+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin", ""]
slug: "rc-day-20"
summary: "I worked on upgrading a Django project from v1 to v4"
---

I have an [open source project](https://github.com/avinassh/della) (check the [screenshots here](https://avi.im/della/)) that used an outdated version of Django. I had made the last commit five years ago. I set out to upgrade Django to the latest version.

## The plan

1. Get it to run.
2. Upgrade to Django 2, then 3, and then 4
3. Ignore backward compatibility of the project. It would help me move fast if I redid the migration if needed.

## Getting it to run

My current Python version is 3.9.7, Postgres is v14, and my first task was to get Della running under these versions. I tried to install the dependencies from `requirements.txt`. The first failure was due to `psycopg2`:

> Error: could not determine PostgreSQL version from '14.0'

I assumed this was because the 2.6.2 version did not support the latest Postgres. Installing the latest 2.9.2 version fixed the issue. Similarly, I also upgraded pillow, gevent and Django (to 1.11.29 LTS). [These changes](https://github.com/avinassh/della/pull/16) were enough to get it running.

## Upgrading to v2

I read the [release note of v2](https://docs.djangoproject.com/en/2.0/releases/2.0/#features-deprecated-in-2-0), but I was unsure how would I make changes in my project because I haven't seen this code in 5 years, and I remember nothing at all. Fortunately, I found this project called [`django-upgrade`](https://github.com/adamchainz/django-upgrade) which applied upgrades automatically. So, I ran it on my project:

```shell
django-upgrade --target-version 2.2 `find . -name "*.py"`
Rewriting ./della/inbox/models.py
Rewriting ./della/inbox/urls.py
Rewriting ./della/gallery/models.py
Rewriting ./della/gallery/urls.py
Rewriting ./della/urls.py
Rewriting ./della/user_manager/models.py
Rewriting ./della/user_manager/urls.py
```

One more nice thing about the `django-upgrade` project is that they nicely mentioned all the breaking changes required. Here are the [changes](https://github.com/avinassh/della/commit/25db8599) it automatically rewrote:

1. `on_delete` argument: Starting with Django 1.9, all foreign key and one to one fields need [`on_delete` argument](https://docs.djangoproject.com/en/3.2/releases/1.9/#foreignkey-and-onetoonefield-on-delete-argument). 

``` python
# added_by = models.ForeignKey(User)
added_by = models.ForeignKey(User, on_delete=models.CASCADE)
# user = models.OneToOneField(User)
user = models.OneToOneField(User, on_delete=models.CASCADE)
```

2. `url` to `path`: [Django 2.0 simplified](https://docs.djangoproject.com/en/2.0/releases/2.0/#simplified-url-routing-syntax) the URL routing syntax. The documentation on [`path`](https://docs.djangoproject.com/en/2.2/ref/urls/) explains how to use them. 

```python
url(r'^upload/$', ImageUploadView.as_view(), name='upload'),
url(r'^(?P<pk>\d+)/$', ImageDetailView.as_view(), name='image-detail'),
url(r'^$', ImageListView.as_view(), name='image-list')
url(r'^@(?P<recipient>[a-zA-Z0-9_]+)/$', ThreadDetailView.as_view()
```

simplified to:
```python
path('upload/', ImageUploadView.as_view(), name='upload'),
path('<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
path('', ImageListView.as_view(), name='image-list')
re_path(r'^@(?P<recipient>[a-zA-Z0-9_]+)/$', ThreadDetailView.as_view()
```

However, when I tried to migrate, I ran into the following error:

```python
File "/Users/avi/code/della/della/urls.py", line 21, in <module>
    from .views import HomePageView
  File "/Users/avi/code/della/della/views.py", line 3, in <module>
    from della.user_manager.forms import SignupForm
  File "/Users/avi/code/della/della/user_manager/forms.py", line 7, in <module>
    from crispy_forms.helper import FormHelper
  File "/Users/avi/.virtualenvs/della/lib/python3.9/site-packages/crispy_forms/helper.py", line 4, in <module>
    from django.core.urlresolvers import reverse, NoReverseMatch
ModuleNotFoundError: No module named 'django.core.urlresolvers'
```

I fixed by [upgrading `django-crispy-forms`](https://github.com/avinassh/della/commit/62781979). The next error was:

```python
File "/Users/avi/code/della/della/urls.py", line 24, in <module>
    path('gallery/', include(
  File "/Users/avi/.virtualenvs/della/lib/python3.9/site-packages/django/urls/conf.py", line 38, in include
    raise ImproperlyConfigured(
django.core.exceptions.ImproperlyConfigured: Specifying a namespace in include() without providing an app_name is not supported. Set the app_name attribute in the included module, or pass a 2-tuple containing the list of patterns and app_name instead.
```

It seems it needed [application name in the urlconfs](https://docs.djangoproject.com/en/2.2/topics/http/urls/#namespaces-and-include). So I [added `app_name` variable](https://github.com/avinassh/della/commit/f222a852) to each of the URLconf module. The next error was:

```python
File "/Users/avi/code/della/della/inbox/urls.py", line 3, in <module>
    from .views import (MessageCreateView, ThreadDetailView, ThreadListView,
  File "/Users/avi/code/della/della/inbox/views.py", line 14, in <module>
    from . import tasks
  File "/Users/avi/code/della/della/inbox/tasks.py", line 4, in <module>
    from django.core.urlresolvers import reverse
ModuleNotFoundError: No module named 'django.core.urlresolvers'
```

Seems they [moved](https://docs.djangoproject.com/en/1.11/ref/urlresolvers/) `reverse` and `reverse_lazy` to `django.urls` from `django.core.urlresolvers`. I simply [renamed the import statements](https://github.com/avinassh/della/commit/41598af) to fix this. Next error was:

```python
  File "/Users/avi/code/della/della/user_manager/urls.py", line 11, in <module>
    path('login/', auth_views.login, name='login',
AttributeError: module 'django.contrib.auth.views' has no attribute 'login'
```

In Django 2.2, `contrib.auth.views` [started using class based views](https://docs.djangoproject.com/en/2.2/topics/auth/default/#all-authentication-views). Following [changes](https://github.com/avinassh/della/commit/5a151b3) fixed this error:

```python
urlpatterns = [
    path('login/', auth_views.login, name='login',
        kwargs={'template_name': 'user_manager/login.html'}),
    path('logout/', auth_views.logout, name='logout',
        kwargs={'next_page': '/'}),
    ]
```

changed to:
```python
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="user_manager/login.html"), name='login',
        ),
    path('logout/', auth_views.LogoutView, name='logout',
        kwargs={'next_page': '/'}),
    ]
```

The following error was:

```python
File "/Users/avi/code/della/della/views.py", line 13, in get_context_data
    if self.request.user.is_authenticated():
TypeError: 'bool' object is not callable
```

Seems `User.is_authenticated()` was [changed to a property](https://docs.djangoproject.com/en/1.10/releases/1.10/#using-user-is-authenticated-and-user-is-anonymous-as-methods) in Django 1.10, but `django-upgrade` did not account for this change. The [fix](https://github.com/avinassh/della/commit/ada5a25) was simple, and now my project started working for Django 2.2.

## Upgrading to v3

`django-upgrade` did not make changes, so I made all changes manually. The first error was:

```python
  File "/Users/avi/.virtualenvs/della/lib/python3.9/site-packages/django/apps/config.py", line 246, in create
    raise ImproperlyConfigured(
django.core.exceptions.ImproperlyConfigured: Cannot import 'user_manager'. Check that 'della.user_manager.apps.UserManagerConfig.name' is correct.
```

It seems Django 3.2 introduced [auto discovery of apps](https://docs.djangoproject.com/en/3.2/releases/3.2/#automatic-appconfig-discovery), which requires [some changes](https://docs.djangoproject.com/en/2.2/ref/applications/#configuring-applications) for the app names. I tried changing the config as per docs; it didn't work. However, I learned that Django made this config optional, so I [removed all of them](https://github.com/avinassh/della/commit/a5eb387). The following error was:

```python
File "/Users/avi/.virtualenvs/della/lib/python3.9/site-packages/django/template/defaulttags.py", line 1036, in find_library
    raise TemplateSyntaxError(
django.template.exceptions.TemplateSyntaxError: 'staticfiles' is not a registered tag library. Must be one of:
admin_list
admin_modify
admin_urls
cache
crispy_forms_field
crispy_forms_filters
crispy_forms_tags
crispy_forms_utils
i18n
l10n
log
static
tz
```

The fix was pretty simple, I just [renamed](https://github.com/avinassh/della/commit/9803d1a) `staticfiles` to `static`. Now my app started working with Django 3.

## Upgrading to v4

At the time of this writing, Django 4.0 RC1 is out, but Django 4.0 [will be out](https://code.djangoproject.com/wiki/Version4.0Roadmap) in just four days.

Only [change required](https://github.com/avinassh/della/commit/cc9cea1) was using the CBV with `as_view`:

```python
path('logout/', auth_views.LogoutView.as_view(), name='logout')
```

Update 7/Dec/2021: Django v4 is out and I upgraded from RC1 to 4.0 final. No changes were required.

## What's next?

Della used a significantly older version of `django-background-tasks` which seems to be unmaintained now. I am looking at alternatives and replacing them.