django-extjs
============

Django [Form][1] and [ModelForm][2] power for your [ExtJs][3] apps. See [ExtJS dual licence][9]

Convert your forms.Form and forms.ModelForm to extjs and handles the form submission like any django form.

Generate custom ExtJs dynamic grids from django querysets. You can also set your grids as Editable.

Tested with ExtJs 3 and Django >= 1 Feedback needed  : <julien@bouquillon.com>

There is a full working demo project based on my django-skeleton here : [ExtJs django-skeleton branch][8] *this is where you should start*.

**Grid example :**

    # the django view
    def users_grid(request):
        # return Json autogrid configuration
        grid = grids.ModelGrid(User)            # generic grid from model fields (can be customised)
        users = User.objects.all()              # use any queryset
        json = grid.to_grid(users, limit = 25)    
        return utils.JsonResponse(json)

    # the javascript (ExtJs 3) :
    var users_grid = new Ext.ux.AutoGrid({
        autoWidth:true
        ,showBbar:true
        ,loadMask:true
        ,store:new Ext.data.JsonStore({
             autoLoad:true
            ,remoteSort:true
            ,proxy:new Ext.data.HttpProxy({
                 url:'apps/main/users_grid'
                ,method:'POST'
            })
        })
    });

    var w = new Ext.Window({
         title:'autogrid !'
        ,items:users_grid
    }).show();
    
**Form example :**

    # the django view

    # the form definition (could also be a ModelForm)
    class ContactForm(forms.Form):
        name = forms.CharField(label='your name')
        phone = forms.CharField(label='phone number', required = False)
        mobile_type = forms.CharField(label='phone type', required = True)
        mobile_type.choices = [
             ('ANDROID','Android')
            ,('IPHONE','iPhone')
            ,('SYMBIAN','Symbian (nokia)')
            ,('OTHERS','Others')
        ]
        email = forms.EmailField(label='your email', initial='test@revolunet.com')
        message = forms.CharField(label='your message', widget = forms.widgets.Textarea(attrs={'cols':15, 'rows':5}))

    ExtJsForm.addto(ContactForm)        # new methods added to the form
            
    # the form view
    def contact_form(request, path = None):
        if request.method == 'POST':
            # handle form submission
            form = ContactForm(request.POST)
            if not form.is_valid():
                return utils.JsonError(form.html_errorlist())
            else:
                # send your email
                print 'send a mail'
            return utils.JsonResponse(utils.JSONserialise({
                'success':True, 
                'messages': [{'icon':'/core/static/img/famfamfam/accept.png', 'message':'Enregistrement OK'}]
                }) )
        else:
            # handle form display
            form = ContactForm()
            return utils.JsonResponse(utils.JSONserialise(form.as_extjsfields()))
            

    # the javascript (ExtJs 3) :
    var contact_win = new Ext.Window({
        title:'django form example'
        ,width:300
        ,y:420
        ,layout:'fit'
        ,height:300
        ,items:new Ext.ux.DjangoForm({
                border:false
                ,intro:'generated contact form'
                ,showButtons:true
                ,showSuccessMessage:'Form submission success'
                ,url:'apps/main/contact_form' 
                ,scope:this
                 ,callback:function(form) {
                    form.doLayout();
                 }
           })
         ,draggable :true
    }).show();
    
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
  
  
**Todo :** 

  - Radio groups
  - Fieldsets : using django  [formsets][6] and [model formsets][7]
  - Grids: gestion editors
  - Grids: auto renderer + editor from choices
  - New FK creation

  
  [1]: http://docs.djangoproject.com/en/dev/topics/forms/
  [2]: http://docs.djangoproject.com/en/dev/topics/forms/modelforms/
  [3]: http://www.extjs.com
  [4]: http://www.extjs.com/forum/showthread.php?t=22661
  [5]: http://github.com/julienb/django-extjs/commit/3fbad2437db07adef645cbf132659932533e1e95#diff-2
  [6]: http://docs.djangoproject.com/en/dev/topics/forms/formsets/
  [7]: http://docs.djangoproject.com/en/dev/topics/forms/modelforms/
  [8]: http://github.com/revolunet/django-skeleton/tree/extjs
  [9]: http://www.sencha.com/products/extjs/license/