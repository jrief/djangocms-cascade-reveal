# DjangoCMS plugin for presentations based on reveal.js

With this plugin, you can benefit from both, (djangoCMS)[https://github.com/divio/django-cms] for
its integrated content editing features and (reveal.js)[https://github.com/hakimel/reveal.js] for
its presentation layer.


## Installation

Steps to setup a running presentation project:

* Create a virtual Python environment and activate it.
* Download and install the project: ``wget -O- https://github.com/jrief/djangocms-reveal/archive/master.tar.gz | tar zx``
* Initialize the project: ``pip install -e djangocms-reveal-master``.

Initialize and populate the database:

```
cd djangocms-reveal-master/demo
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

## Usage

Point a browser onto http://localhost:8000/admin/ and sign in using the chosen credentials.

Create a new CMS page with the template named *Reveal Presentation*. View this page on site and
change into **Structure** mode. Add one or more plugins named **Section** below the placeholder
**Presentation Slides**. As children of a **Section** plugin chose **Fragment**, **Speaker Note**,
**Mark Down** or a sub-**Section** plugin.

The meaning of these plugins is explained in the docs of **reveal.js**. 

### Global Options for reveal.js

On the toolbar, below the main menu, locate the item **Reveal...**. Here you can change the global
settings of a Reveal presentation.

