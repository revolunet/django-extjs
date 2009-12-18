django-extjs
============

Django [Form][1] and [ModelForm][2] power in your [ExtJs][3] apps

Convert your forms.Form and forms.ModelForm to extjs and handles the form submission like any django form.

Generate custom ExtJs dynamic grids from django models.

Tested with ExtJs 3 and Django >= 1 Feedback needed  : <julien@bouquillon.com>

(used to work with ExtJs 1.2  (this [commit][5] may have broken this, not tested)


**Usage :**

  - Clone the Git repo and create a django_extjs app in your django project
  - eg: git submodule add  -- "git://github.com/julienb/django-extjs.git"  "apps/django_extjs"
  - Put static folder somewhere on your statics
  - Create an example view from views.py
  - Edit static/example.html to match your view and static paths
  - Open your form from ExtJs:
  
        // simplest example of a django generated Form (EmailFormExample)
        // its ajax loaded then displayed in a new window
        function openForm() {
         // we first declare a window where the form will appear
          var window_form = new Ext.Window({
                title:'simple django Form'
                ,autoWidth:true
                ,autoScroll:true
                ,autoHeight:true
            });
          // then we ask our form to load and display the window when done
          var django_form = new Ext.ux.DjangoForm({url:'/apps/django_extjs/example_email', callback:function(form) {window_form.add(form);window_form.show();}});
          // we want to auto close the window on form submit success
          django_form.on('submitSuccess', function() {
                    window_form.close();
                });
        }
             
  
**The lib provides :**

  - Django code to render your forms as extjs
  - ExtJs helpers to load/save your forms and models
  - Django code to generate full json to render ExtJS grids with paging (metaData + data)
  - A special ExtJs json parser (special ExtJs keywords handling)

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

  - The lib includes [Saki's Ext.ux.form.DateTime][4] ExtJs component (LGPL)
  - Also includes Ext.ux.AutoGrid and Ext.ux.AutoGridPanel
  
  
**Todo :** 

  - Radio groups
  - Fieldsets
  - New FK creation

  
  [1]: http://docs.djangoproject.com/en/dev/topics/forms/
  [2]: http://docs.djangoproject.com/en/dev/topics/forms/modelforms/
  [3]: http://www.extjs.com
  [4]: http://www.extjs.com/forum/showthread.php?t=22661
  [5]: http://github.com/julienb/django-extjs/commit/3fbad2437db07adef645cbf132659932533e1e95#diff-2
 