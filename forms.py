# -*- encoding: UTF-8 -*-


from django import forms

CHAR_PIXEL_WIDTH = 8
CHAR_PIXEL_HEIGHT = 15

import utils

 
def DateField_ExtJs_clean(value):
    if value == '': return None
    value = value.split('T')[0]
    return value

def DateTimeField_ExtJs_clean(value):
    if value == '': return None
    value = value.replace('T', ' ')
    return value

def TimeField_ExtJs_clean(value):
    if value == '': return None
    #value = value.split('T')[1]
    return value
    
def getExtJsModelForm(modelref, exclude_list  = [], fields_list = []):
    class FormFromModel(forms.ModelForm):
        class Meta:
            model = modelref
            exclude = exclude_list 
            fields = fields_list
        def __init__(self, *args, **kwargs):
            super(FormFromModel, self).__init__(*args, **kwargs)
             
    ExtJsForm.addto(FormFromModel)
    
    # override Field.clean for date fields and ExtJs formats
    for item in FormFromModel.base_fields:
         #print 'class field', item, FormFromModel.base_fields[item]
         o = FormFromModel.base_fields[item]
         if o.__class__.__name__ in ['DateField','DateTimeField','TimeField']:
            o.clean = globals()['%s_ExtJs_clean' % o.__class__.__name__]
            
    return FormFromModel

def getFieldConfig(field_name, django_field, value = None):
   # print 'getFieldConfig', field_name
    ofield = django_field
    form_field = django_field
    field_class_name = ofield.__class__.__name__ 
    if not isinstance(ofield, forms.Field):
        form_field = ofield.formfield()
        
    config = {}
    
    if value:
        config['value'] = value
    elif hasattr(ofield, 'initial'):
        config['value'] = ofield.initial

    
    config['name'] = u'%s' % field_name
    config['fieldLabel'] = u'%s' % (form_field and form_field.label or field_name)
    if form_field:
        config['allowBlank'] = not(form_field.required)
        config['required'] = form_field.required
    
    e = getattr(ofield, 'widget', None)
    if e:
        #print 'e', e
        s = ofield.widget.attrs.get('style', None)
        if s:
            config['style'] = s
                 
        # width based on django widget 'size' attr
        v = ofield.widget.attrs.get('size', None)
        if v:
            config['width'] = v * CHAR_PIXEL_WIDTH
            
    
        
   # print field_name, field_class_name
    
    if field_class_name == 'HiddenInput':
        config['xtype'] = 'hidden'
        config['name'] = field_name
    
    # foreignkeys or custom choices
    elif field_class_name in ['ForeignKey', 'ModelChoiceField', 'TypedChoiceField'] or getattr(ofield, 'choices', None):
        config['xtype'] = 'combo' 
        config['blankText'] = field_name + ' :' 
        # removes the standard '-----'
        form_field.empty_label = None
        choices = form_field.choices
        #print field_class_name, form_field.choices
        #for i in form_field.choices:
         #   print i
        choices = [[c[0], c[1]] for c in choices]
        # if field_class_name == 'ForeignKey' and not getattr(ofield, 'choices', None):
            # choices = [[c[0], c[1]] for c in ]
        
        
        config['store'] = "new Ext.data.SimpleStore({fields: ['id','display'],  data : %s })" % ( utils.JSONserialise(choices))
        config['valueField'] = 'id'
        config['displayField'] = 'display'
        config['hiddenName'] = field_name
        if field_class_name in ['ModelChoiceField', 'TypedChoiceField'] : 
            # disable foreignkeys edition
            config['editable'] = True
            config['forceSelection'] = True
            config['typeAhead'] = True
        config['mode'] = 'local'
        config['triggerAction'] = 'all'
        
    # number field
    elif field_class_name in ['DecimalField', 'FloatField', 'IntegerField', 'PositiveIntegerField', 'PositiveSmallIntegerField']:
        config['xtype'] = 'numberfield'
        if  isinstance(ofield, forms.IntegerField):
            config['allowDecimals'] = False
            # if ofield.__class__.__name__ in ['PositiveIntegerField', 'PositiveSmallIntegerField']:
            #, 'PositiveSmallIntegerField']:
                # extfield['allowNegative'] = False
        else:
            config['allowDecimals'] = True
            config['decimalPrecision'] = 2
            config['decimalSeparator'] = '.'                   
 
    # textfield
    elif field_class_name in ['CharField', 'TextInput', 'Textarea']:
        config['xtype'] = 'textfield'
        if hasattr(ofield, 'widget'):
            if isinstance(ofield.widget, forms.widgets.PasswordInput):
                config['inputType'] = 'password'
            elif isinstance(ofield.widget, forms.widgets.Textarea):
                config['xtype'] = 'textarea'
                v = ofield.widget.attrs.get('cols', None)
                if v:
                    config['width'] = int(v) * CHAR_PIXEL_WIDTH 
                v = ofield.widget.attrs.get('rows', None)
                if v:
                    config['height'] = int(v) * CHAR_PIXEL_HEIGHT
            if ofield.min_length:
                config['minLength'] = ofield.min_length 
            if ofield.max_length:
                config['maxLength'] = ofield.max_length
 
    elif field_class_name == 'DateField':
        config['xtype'] = 'datefield'
        dformat = form_field.input_formats
        if dformat:
            dformat = dformat[0]
        config['format'] = utils.DateFormatConverter(to_extjs = dformat)
        #config['hiddenFormat'] = utils.DateFormatConverter(to_extjs = form_field.input_formats[0])
    elif field_class_name == 'TimeField':
        config['xtype'] = 'timefield'
        config['increment'] = 30
        dformat = form_field.input_formats
        if dformat:
            dformat = dformat[0]
       # config['hiddenFormat'] = utils.DateFormatConverter(to_extjs = form_field.input_formats[0])
        config['format'] = utils.DateFormatConverter(to_extjs = dformat)
        config['width'] = 60
        config['value'] = value and value.strftime(ofield.input_formats[0]) or ''
    # datetime : use sakis xdatetime ext.ux
    elif field_class_name == 'DateTimeField':
        config['xtype'] = 'xdatetime'
        # todo : ugly !!
        datef = timef = date_format = None
        
        if form_field.input_formats:
            date_format = form_field.input_formats[0]
            (datef, timef) = date_format.split(' ')
        config['timeFormat'] = utils.DateFormatConverter(to_extjs = timef)
        config['timeWidth']  = 60
        config['dateWidth']  = 100
        config['dateFormat'] = utils.DateFormatConverter(to_extjs = datef)
        if date_format:
            config['hiddenFormat'] = utils.DateFormatConverter(to_extjs = date_format)
        if value:
           # config['value'] = value
            config['dateConfig'] = {'value':value.strftime(datef)}
            config['timeConfig'] = {'value':value.strftime(timef)}
        else:
            #config['value'] = ''
            config['dateConfig'] = {'value':''}
            config['timeConfig'] = {'value':''}
        
    elif ofield.__class__.__name__ == 'URLField':
        config['xtype'] = 'textfield'
        config['vtype'] = 'url'
    elif ofield.__class__.__name__ == 'EmailField':
        config['xtype'] = 'textfield'
        config['vtype'] = 'email'
    elif ofield.__class__.__name__ in ['BooleanField', 'CheckboxInput']:
        config['xtype'] = 'checkbox'
        if value:
            config['value'] = value
            config['checked'] = value

    # the field.ext attribute can be used as an dict overrider if needed
    e = getattr(ofield, 'ext', None)
    if e:
        config.update(e)
            
    return config
    
class ExtJsField(object):
    def __init__(self, field_name, django_field):
        self.config = {}
        # set some default config options at init
        self.config['name'] = u'%s' % field_name
        self.config['fieldLabel'] = u'%s' % (django_field.label or field_name)
        self.config['allowBlank'] = not(django_field.required)
        self.config['invalidText'] = u'%s' % django_field.help_text or ''
        # init the value if any
        self.config['value'] = ''
        if django_field.initial:
            self.config['value'] = django_field.initial
        # apply html style if any
        #print django_field.widget
        s = django_field.widget.attrs.get('style', None)
        if s:
           self.config['style'] = s
        # width based on django widget 'size' attr
        v = django_field.widget.attrs.get('size', None)
        if v:
            self.config['width'] = v * CHAR_PIXEL_WIDTH           
        # override any config provided in the field definition
        e = getattr(django_field, 'ext', None)
        if e:
            for item in e.keys():
                self.config[item] = e[item]
                
    def getConfig(self):
        return self.config
 
   
                
        
class ExtJsForm(object):
    """ 
        .add a as_extjs method to forms.Form or forms.ModelForm; this method returns a formpanel json config, with all fields, buttons and logic
        .add a as_extjsfields method that returns only the field list. useful if you want to customise the form layout
        .add a html_errorlist to return form validations error for an extjs window
    """
     
    
    @classmethod
    def addto(self, cls):
        cls.as_extjsfields = self.as_extjsfields
        cls.as_extjs = self.as_extjs
        cls.html_errorlist = self.html_errorlist
        # default submit handler 
        handler_submit = "function(btn) {console.log(this, btn);this.findParentByType(this.form_xtype).submitForm()}"
        handler_reset = "function(btn) {console.log(this, btn);this.findParentByType(this.form_xtype).resetForm()}"
        cls.ext_baseConfig = {
        }
        
    @staticmethod
    def as_extjs(self, excludes = []):
        config = ""
        config_dict = self.ext_baseConfig
        if getattr(self, 'ext_config', None):
            config_dict.update(self.ext_config)
        config_dict['items'] = self.as_extjsfields(excludes = excludes)
        #if len(config_dict.items())>0:
            #config = utils.JSONserialise(config_dict)
        return utils.JSONserialise(config_dict)
        
    @staticmethod
    def html_errorlist(self):
        html = ''
        for field, err in self.errors.items():
            html += '<br><b>%s</b> : %s' % (field, err.as_text())
        return html
        
    @staticmethod
    def as_extjsfields(self, excludes = []):
            ext_fields = []
            
            if getattr(self, 'intro', None):
                ext_fields.append({'style':'padding:5px', 'html':self.intro})
            
            # TODO :
            # fieldsets
            # htmlfield
            # radiogroups
            # decimal : max_digits, decimal_places, negative
            # number formatting

            
            for field in self.fields:
                if field in excludes: continue
                ofield = self.fields[field]

                value = getattr(self, 'instance', None) and getattr(self.instance, field) or None
                if value and ofield.__class__.__name__ == 'ModelChoiceField':
                        value = getattr(self.instance, field).pk
                        
                extfield = getFieldConfig(field, ofield, value)
                #print 'getFieldConfig', extfield
                
                ext_fields.append(extfield)   
                
            return ext_fields
           