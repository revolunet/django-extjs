django-extjs-forms
==================

Django Form and ModelForm power in your ExtJs apps

Convert your forms.Form and forms.ModelForm to extjs and handles the form submission like any django form.

Tested with ExtJs 1.2 and Django 1.0.2. Feedback needed !


**Usage :**
  - Put django_extjs on your python path
  - Put static dir somewhere on your statics
  
  
**The lib provides :**

  - Django code to render your forms as extjs
  - ExtJs helpers to load/save your forms and models
  - A special ExtJs json parser

**Features :**

  - Compatible with Form and ModelForm
  - Convert django form fields and widgets to Ext.form fields
  - Handles date formats, foreignkeys, choicefields
  - Handles vtypes, required
  - You can add an 'intro' text to an self-generated form
  - Ajax submits and django validations error messages
  - Forms can be ajax loaded or not

**Flexibility :**

  - You can add fields you need
  - You can render a full self generated form in ExtJs
  - Or create a custom ExtJs form using django fields
  - You can ajax load (or not) your form and inlude it in any Ext component
  - ExtJs code fully overridable

**Dependencies :**

  - The lib includes [Saki's Ext.ux.form.DateTime][1] ExtJs component (LGPL)
  
  
**Todo :** 

  - Radio groups
  - New FK creation

  
  
  
  [1]: http://www.extjs.com/forum/showthread.php?t=22661
 