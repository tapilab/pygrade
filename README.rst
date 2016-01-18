===============================
pygrade
===============================

.. image:: https://img.shields.io/pypi/v/pygrade.svg
        :target: https://pypi.python.org/pypi/pygrade

.. image:: https://img.shields.io/travis/tapilab/pygrade.svg
        :target: https://travis-ci.org/tapilab/pygrade

.. image:: https://readthedocs.org/projects/pygrade/badge/?version=latest
        :target: https://readthedocs.org/projects/pygrade/?badge=latest
        :alt: Documentation Status


auto-grade python assignments

* Free software: ISC license
* Documentation: https://pygrade.readthedocs.org.

This library helps one create and grade programming assignments written in Python and submitted by students via Github.

Features include the ability to:

- Create private GitHub repositories for each student.
- Populate student repositories with starter code.
- Create student assignments by running unittests against their code.
- Different point values can be assigned to each test
- Grades and failing tests are pushed back to the student repositories.

See the example_ for a tutorial on usage.

.. _example: https://github.com/tapilab/pygrade/tree/master/example

Related libraries
-----------------

* teacherspet_ : manipulates github repos for teaching.

.. _teacherspet: https://github.com/education/teachers_pet

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
