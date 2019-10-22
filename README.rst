=================
Django Setup Demo
=================
In some django project I use the python setuptools deployment. So I can run::

  python setup.py install

to install the project. For this to work you need to make some adjustments.
While I write the following lines, I recognize that every step make only a small
advantage. But seeing how everything works together really makes me happy.

The demo django project in this example is called mysite. You have to replace
that with you project name.


0. Create the project
---------------------
Skip this if you know how to setup a django project. If you are new to
`python <https://docs.python.org/3/tutorial/>`_
or `django <https://www.djangoproject.com/start/>`_, read the documentation.
Some fast tips you should check out if you do not know that this is.

1. Do not uses python 2.7
2. Use a virtual environment for your project.
3. Write useful tests.


1. Setup.py
-----------
Add the setup.py file to the root of your project. The file should look like
this::

  from setuptools import setup, find_packages


  if __name__ == '__main__':
      setup(
          name='mysite',
          version='1.0',
          packages=find_packages(),
      )

You can add more information like a description, the author, etc. see the
`official documentation <https://packaging.python.org/tutorials/packaging-projects/>`_
for more.

Now you can install your project to the system packages or rather the virtual
environment. Your django project is now a python package.

**Benefit:** You can import your project/package everywhere. This could be
interesting if you want to load the wsgi application. It is no longer necessary
to specify the project directory.


2. Move the manage.py file
--------------------------
Move the manage.py file from the root directory to the project folder. The
folder with the settings.py, urls.py, etc. files. Then rename it to "__main__.py"

This make only a small advantage, but I like if every thing is in one place. And
it make the next step much nicer.

**Benefit:** To work with your project you have to use the "manage.py" file. For
that you have to be in the root directory. Now you can run::

  python -m mysite runserver

instead of::

  python -m manage.py runserver

and it makes no difference in which directory you are. Unless you want to create
a new app. Then you have to be inside the root directory.


3. Use the setuptools entry points
----------------------------------
The setuptools make it easy to write a command line program. Add the "manage.py"
file (now the "__main__.py" file) to the setup::

  if __name__ == '__main__':
      setup(
          ...
          entry_points={
              'console_scripts': [
                  'mysite=mysite.__main__:main',
              ],
          },
          ...
      )

**Benefit:** Now instead of::

  python -m mysite migrate

run::

  mysite migrate

Not that big advantage, but I like how every thing work together.


4. Setup the install requirements
---------------------------------
Almost every django project have a "requirements.txt" file which include all
packages to setup the project. To avoid the file, add the dependencies into the
setup script::

  if __name__ == '__main__':
      setup(
          ...
          install_requires=[
              'django',
              ...
          ],
          ...
      )

**Benefit:** Avoid the "requirements.txt" file and setuptools manage the
dependencies. Run::

  python setup.py install

and everything is installed as expected.


5. Uses SCM metadata for the versions
-------------------------------------
This is not only a django thing. It woke on every python package. The
`setuptools_scm <https://github.com/pypa/setuptools_scm>`_ package take the
version information from SCM metadata tags. To set it up change the setup
script::

  if __name__ == '__main__':
      setup(
          ...
          # version='1.0',  <<< You can remove the version
          use_scm_version=True,
          setup_requires=[
              'setuptools_scm',
          ],
          ...
      )

To access the version number in your project add the flowing to the
"__init__.py" file::

  from pkg_resources import get_distribution, DistributionNotFound

  try:
      __version__ = get_distribution(__name__).version
  except BaseException:
      __version__ = 'unknown'
  finally:
      del get_distribution, DistributionNotFound

**Benefit:** Do I really need to tell you why that is so good? You get the
version from the git tags. This is amazing. Write a context processors and add
the version (from mysite import __version__) to the footer.


6. Templates and static files
-----------------------------
This are none python files. So you have to add then to the project. Create a
"MANIFEST.in" file in the root directory with::

  recursive-include mysite/static *
  recursive-include mysite/templates *

And setup the django project to work this this folders. Change the
"mysite/settings.py" file::

  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
  ...
  TEMPLATES = [
      {
          ...
          'DIRS': [
              os.path.join(BASE_DIR, 'templates'),
          ],
          ...
      }
  ]
  ...
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(WORK_DIR, 'db.sqlite3'),
      }
  }

Now you can add the templates in "mysite/templates" and the static file in
"mysite/static".

**Benefit:** Not a really benefit, but now everything is in one folder.
