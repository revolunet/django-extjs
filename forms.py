# -*- encoding: UTF-8 -*-


from django import forms

CHAR_PIXEL_WIDTH = 8
CHAR_PIXEL_HEIGHT = 15

import utils


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
    def as_extjs(self):
        config = ""
        config_dict = self.ext_baseConfig
        if getattr(self, 'ext_config', None):
            config_dict.update(self.ext_config)
        config_dict['items'] = self.as_extjsfields()
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
    def as_extjsfields(self):
            ext_fields = []
            
            if getattr(self, 'intro', None):
                ext_fields.append({'style':'padding:5px', 'html':self.intro})
            
            # TODO :
            # fieldsets
            # htmlfield
            # radiogroups
            # decimal : max_digits, decimal_places, negative
            # number formatting
            #if getattr(self, 'instance', None):
                #for lfield in self.instance._meta.fields: 
                    #print 'FIELD INSTANCE :', lfield
                    #print dir(lfield)
            for field in self.fields:
                ofield = self.fields[field]
                #print dir(ofield)
                #print dir(ofield)
                #print '************',field, ofield
                extfield = None
                defaultConfig = {}
                defaultConfig['name'] = field
                defaultConfig['fieldLabel'] = ofield.label or field
                defaultConfig['allowBlank'] = not(ofield.required)
                
                defaultConfig['value'] = ''
                if self.initial.get(field, '') not in ['', None]:
                    defaultConfig['value'] = self.initial[field]
                elif ofield.initial:
                    defaultConfig['value'] = ofield.initial
        
                s = ofield.widget.attrs.get('style', None)
                if s:
                    defaultConfig['style'] = s
                    
              #  print field, 'initial', ofield.initial, self.initial.get(field, ''), '---'
              
                # field specific ext params
                e = getattr(ofield, 'ext', None)
                if e:
                    for item in e.keys():
                        defaultConfig[item] = e[item]
                         
                # width based on django widget 'size' attr
                v = ofield.widget.attrs.get('size', None)
                if v:
                    defaultConfig['width'] = v * CHAR_PIXEL_WIDTH
                    
                    
                # hidden
                if ofield.widget.__class__.__name__ == 'HiddenInput':
                    extfield = {}
                    extfield['xtype'] = 'hidden'
                    extfield['name'] = field
                    extfield['value'] = ofield.initial or ''
                    if getattr(self, 'instance', None) and getattr(self.instance, field):
                        extfield['value'] = getattr(self.instance, field)
                    ext_fields.append(extfield)
                
                # foreignkeys or custom choices
                elif ofield.__class__.__name__ in ['ModelChoiceField', 'TypedChoiceField'] or getattr(ofield, 'choices', None):
                    extfield = defaultConfig.copy()
                    extfield['xtype'] = 'combo' 
                    extfield['blankText'] = field + ' :' 
                    choices= [[c[0], c[1]] for c in ofield.choices]
                    extfield['store'] = "new Ext.data.SimpleStore({fields: ['id','display'],  data : %s })" % ( utils.JSONserialise(choices))
                    extfield['displayField'] = 'display'
                    extfield['valueField'] = 'id'
                    extfield['hiddenName'] = field
                    if ofield.__class__.__name__ == 'ModelChoiceField': 
                        extfield['editable'] = False
                        extfield['forceSelection'] = True
                    extfield['mode'] = 'local'
                    extfield['triggerAction'] = 'all'
                    from django.core.exceptions import ObjectDoesNotExist
                    try:
                        if getattr(self, 'instance', None) and getattr(self.instance, field, None):
                            if ofield.__class__.__name__ == 'ModelChoiceField':
                                extfield['value'] = getattr(self.instance, field).pk
                            else:
                                extfield['value'] = u'%s' % getattr(self.instance, field)
                    except ObjectDoesNotExist:
                           extfield['value'] = ''
                                
    
                    ext_fields.append(extfield)
                    
                # number field
                elif ofield.__class__.__name__ in ['DecimalField', 'FloatField', 'IntegerField', 'PositiveIntegerField', 'PositiveSmallIntegerField']:
                    extfield = defaultConfig.copy()
                    
                    extfield['xtype'] = 'numberfield'
                    if getattr(self, 'instance', None) and getattr(self.instance, field):
                        extfield['value'] = getattr(self.instance, field)
                    if  isinstance(ofield, forms.IntegerField):
                        
                        extfield['allowDecimals'] = False
                        # if ofield.__class__.__name__ in ['PositiveIntegerField', 'PositiveSmallIntegerField']:
                        #, 'PositiveSmallIntegerField']:
                            # extfield['allowNegative'] = False
                    else:
                        extfield['allowDecimals'] = True
                        extfield['decimalPrecision'] = 2
                        extfield['decimalSeparator'] = '.'                   
                    ext_fields.append(extfield)
                # textfield
                elif ofield.__class__.__name__ == 'CharField':
                    extfield = defaultConfig.copy()
                    extfield['xtype'] = 'textfield'
                    if  isinstance(ofield.widget, forms.widgets.PasswordInput):
                            extfield['inputType'] = 'password'
                    if  isinstance(ofield.widget, forms.widgets.Textarea):
                        extfield['xtype'] = 'textarea'
                        v = ofield.widget.attrs.get('cols', None)
                        if v:
                            extfield['width'] = int(v) * CHAR_PIXEL_WIDTH 
                            #print extfield['width']
                        v = ofield.widget.attrs.get('rows', None)
                        if v:
                            extfield['height'] = int(v) * CHAR_PIXEL_HEIGHT
                            #print extfield['height']
                    if ofield.min_length:
                        extfield['minLength'] = ofield.min_length 
                    if ofield.max_length:
                        extfield['maxLength'] = ofield.max_length
                    if getattr(self, 'instance', None) and getattr(self.instance, field, None):
                        extfield['value'] = getattr(self.instance, field)
                    ext_fields.append(extfield)
                elif ofield.__class__.__name__ == 'DateField':
                    extfield = defaultConfig.copy()
                    extfield['xtype'] = 'datefield'
                    extfield['format'] = utils.DateFormatConverter(to_extjs = ofield.input_formats[0])
                    if getattr(self, 'instance', None) and getattr(self.instance, field, None):
                        dval = getattr(self.instance, field)
                    ext_fields.append(extfield)
                elif ofield.__class__.__name__ == 'URLField':
                    extfield = defaultConfig.copy()
                    extfield['xtype'] = 'textfield'
                    extfield['vtype'] = 'url'
                    if getattr(self, 'instance', None) and getattr(self.instance, field, None):
                        extfield['value'] = getattr(self.instance, field)
                    ext_fields.append(extfield)
                elif ofield.__class__.__name__ == 'TimeField':
                    extfield = defaultConfig.copy()
                    extfield['xtype'] = 'timefield'
                    extfield['increment'] = 30
                    extfield['format'] = utils.DateFormatConverter(to_extjs = ofield.input_formats[0])
                    extfield['width'] = 60
                    if getattr(self, 'instance', None) and getattr(self.instance, field, None):
                        try:
                            extfield['value'] = getattr(self.instance, field).strftime(ofield.input_formats[0])
                        except ValueError:
                            #extfield['value'] = None
                            pass
                    ext_fields.append(extfield)
                # datetime : use sakis xdatetime ext.ux
                elif ofield.__class__.__name__ == 'DateTimeField':
                    extfield = defaultConfig.copy()
                    extfield['xtype'] = 'xdatetime'
                  #  print 'xdatetime', ofield.initial, extfield['value'] 
                    # todo : ugly !!
                    date_format = ofield.input_formats[0]
                    (datef, timef) = date_format.split(' ')
                    extfield['timeFormat'] = utils.DateFormatConverter(to_extjs = timef)
                    extfield['timeWidth']  = 60
                    extfield['dateWidth']  = 100
                    extfield['dateFormat'] = utils.DateFormatConverter(to_extjs = datef)
                    extfield['hiddenFormat'] = utils.DateFormatConverter(to_extjs = date_format)
                    #print field, 'format:', date_format, datef, timef
                    if getattr(self, 'instance', None) and getattr(self.instance, field, None):
                        try:
                            extfield['value'] = getattr(self.instance, field).strftime(date_format)
                            extfield['dateConfig'] = {'value':getattr(self.instance, field).strftime(datef)}
                            extfield['timeConfig'] = {'value':getattr(self.instance, field).strftime(timef)}
                        except ValueError:
                            extfield['value'] = 0
                            extfield['dateConfig'] = {'value':0}
                            extfield['timeConfig'] = {'value':0}
                    else:
                        if extfield['value'].__class__.__name__ == 'datetime':
                            extfield['dateConfig'] = {'value':extfield['value'].strftime(datef)}
                            extfield['timeConfig'] = {'value':extfield['value'].strftime(timef)}
                            extfield['value'] = extfield['value'].strftime(date_format)
                        else:
                            extfield['value'] = ''
                            extfield['dateConfig'] = {'value':''}
                            extfield['timeConfig'] = {'value':''}
                    ext_fields.append(extfield)                
                # email
                elif ofield.__class__.__name__ == 'EmailField':
                    extfield = defaultConfig.copy()
                    extfield['xtype'] = 'textfield'
                    extfield['vtype'] = 'email'
                    if getattr(self, 'instance', None) and getattr(self.instance, field, None):
                        extfield['value'] = getattr(self.instance, field)
                    ext_fields.append(extfield)
                # checkboxes
                elif ofield.__class__.__name__ == 'BooleanField':
                    extfield = defaultConfig.copy()
                    extfield['xtype'] = 'checkbox'
                    if getattr(self, 'instance', None) and getattr(self.instance, field, None):
                        extfield['value'] = getattr(self.instance, field)
                        extfield['checked'] = getattr(self.instance, field)
                    else:
                        extfield['checked'] = ofield.initial
                    ext_fields.append(extfield)

            return ext_fields
