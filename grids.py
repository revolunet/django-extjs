 
import utils

import forms

# width, dateFormat, renderer, hidden, align, type


class SimpleGrid(object):
    def to_grid(self, fields, rows, totalcount = None, json_add = {}, sort_field = 'id', sort_direction = 'DESC'):
        if not totalcount: 
            totalcount = len(rows)
        jdict = {
            'success':True
           ,'metaData':{
                'root':'rows'
                ,'totalProperty':'totalCount'
                ,'successProperty':'success'
                ,'sortInfo':{
                   'field': sort_field
                   ,'direction': sort_direction
                }
                ,'fields':fields
                }
                ,'rows':rows
                ,'totalCount':totalcount
            }
        return utils.JSONserialise(jdict)
         

class VirtualField(object):
    def __init__(self, name):
        self.name = name


        
class ModelGrid(object):

    def __init__(self, model):
        self.model = model      # the model to use as reference
        self.fields = []        # holds the extjs fields
        self.base_fields = []   # holds the base model fields
        
        model_fields = self.model._meta._fields()
        excludes = getattr(self.Meta, 'exclude', [])
        # reorder cols if needed
        order = getattr(self.Meta, 'order', None)
        if order and len(order) > 0:
            for field in order:
                added = False
                for f in model_fields:
                    if f.name == field:
                        added = True
                        self.base_fields.append(f)
                if not added:
                    self.base_fields.append(VirtualField(field))
        else:
            self.base_fields = model_fields
            
        
        for field in self.base_fields:
            if field.name in excludes:
                continue
            if field.__class__.__name__ == VirtualField:
                self.fields.append(self.Meta.fields_conf[field.name])
                continue
            fdict = {'name':field.name, 'header': field.name}
            if field.name == 'id':
                fdict['id']='id'
            if  field.__class__.__name__ == 'DateTimeField':
                fdict['type'] = 'datetime'
                fdict['dateFormat'] = 'Y-m-d H:i:s'
                fdict['format'] = 'Y-m-d H:i:s'
                #fdict['editor'] = "new Ext.ux.form.DateTime({hiddenFormat:'Y-m-d H:i', dateFormat:'Y-m-D', timeFormat:'H:i'})"
            if  field.__class__.__name__ == 'DateField':
                fdict['type'] = 'date'
                fdict['dateFormat'] = 'Y-m-d'
                fdict['format'] = 'Y-m-d'
                #fdict['editor'] = "new Ext.form.DateField({format:'Y-m-d'})"
            elif field.__class__.__name__ == 'IntegerField':
                fdict['type'] = 'int'
                #fdict['editor'] = 'new Ext.form.NumberField()'
            elif field.__class__.__name__ == 'BooleanField':
                fdict['type'] = 'boolean'
                #fdict['editor'] = 'new Ext.form.Checkbox()'
            elif field.__class__.__name__ == 'DecimalField':
                fdict['type'] = 'float'
                fdict['renderer'] = 'function(v) {return (v.toFixed && v.toFixed(2) || 0);}'
                #fdict['editor'] = 'new Ext.form.NumberField()'
            elif  field.__class__.__name__ == 'ForeignKey':
                pass
            if getattr(self.Meta, 'fields_conf', {}).has_key(field.name):
                fdict.update(self.Meta.fields_conf[field.name])
                
               # print fdict
            self.fields.append(fdict)
        #for field in self.model:
        #    print field
    
    def get_field(self, name):  
        for f in self.fields:
            if f.get('name') == name:
                return f
        return None
    def get_base_field(self, name):  
        for f in self.base_fields:
            if f.name == name:
                return f
        return None
    def get_fields(self, colModel):  
        """ return this grid field list
            . can include hidden fields
            . A given colModel can order the fields and override width/hidden properties
        """
        # standard fields
        fields = self.fields
        # use the given colModel to order the fields
        if colModel and colModel.get('fields'):
            fields = []
            for f in colModel['fields']:    
                for cf in self.fields:
                    if cf['name'] == f['name']:
                        config_field = cf
                        if f.get('width'):
                            config_field['width'] = f.get('width')
                        # force hidden=False if field present in given colModel
                        if f.get('hidden') == True:                        
                            config_field['hidden'] = True
                        else:
                            config_field['hidden'] = False
                        fields.append(config_field)
        return fields
                        
    def get_rows(self, fields, queryset, start, limit):
        """ 
            return the row list from given queryset 
            order the data based on given field list
            paging from start,limit
        """
        rows = []
        if queryset:
            if limit > 0:
                queryset = queryset[int(start):int(start) + int(limit)]
            fields_items = []
            for item in queryset:
                field_items = []
                rowdict = {}
                for field in fields:
                    val = getattr(item, field['name'], '')
                    if val:
                        if field.get('type', '') == 'date':
                            val = val.strftime(utils.DateFormatConverter(to_python = field['dateFormat'] ) )
                        elif field.get('type', '') == 'datetime':
                            val = val.strftime(utils.DateFormatConverter(to_python = field['dateFormat'] ) )
                        else:
                            val = utils.JsonCleanstr(val)
                    else:
                        if field.get('type', '') == 'float':
                            val = 0.0
                        elif field.get('type', '') == 'int':
                            val = 0
                        else:
                            val = ''
                    #astr = utils.JSONserialise_dict_item(field['name'], val)
                    rowdict[field['name']] = val
                    #field_items.append(astr)
                #fields_items.append('{%s}' % ','.join(field_items))
                rows.append(rowdict)
            #json += ','.join(fields_items)
            #json += ']\n'

        return rows
         
        
    def to_grid(self, queryset, start = 0, limit = 0, totalcount = None, json_add = {}, colModel = None, sort_field = 'id', sort_direction = 'DESC'):
        """ return the given queryset as an ExtJs grid config
            includes full metadata (columns, renderers, totalcount...)
            includes the rows data
            to be used in combination with Ext.ux.AutoGrid 
        """
        if not totalcount: 
            totalcount = queryset.count()

        base_fields = self.get_fields(colModel)
        
        # todo : stupid ?
        id_field = base_fields[0]['name']
            
        jsondict = {
             'succes':True
            ,'metaData':{
                 'root':'rows'
                ,'totalProperty':'totalCount'
                ,'successProperty':'success'
                ,'idProperty':id_field
                ,'sortInfo':{
                   "field": sort_field
                   ,"direction": sort_direction
                }
                ,'fields':base_fields
            }
            ,'rows':self.get_rows(base_fields, queryset, start, limit)
            ,'totalCount':totalcount
        }
        
        if json_add:
            jsondict.update(json_add)
        
        return utils.JSONserialise(jsondict) 
        
    class Meta:
        exclude = []
        order = []
        fields_conf = {}

class EditableModelGrid(ModelGrid):
    def __init__(self, *args, **kwargs):
        super(EditableModelGrid, self).__init__(*args, **kwargs)
        # add editors
        for field in self.base_fields:
            field_conf = self.get_field(field.name)
            if not (getattr(self.Meta, 'fields_conf', {}).has_key(field.name) and self.Meta.fields_conf[field.name].has_key('editor')):
                field_conf['editor'] = forms.getFieldConfig(field.name, field)
                
    def update_instances_from_json(self, json, insert_new = True):
        """ udpate this grid model instances from provided json
            json example : update=[{"id":1, "username":"root2","first_name":"", "last_name":"bouqui", "is_staff":false, "is_superuser":true}]
            only modified data is sent from client
        """
        from django.utils import simplejson
        items = simplejson.loads(json)
        
        forms_items = []
        forms_valid = True
        errors = []
        for item_data in items:
            # get instance for this line
            # todo : dynamic pk
            pk = item_data.get('id', None)
            form_data = item_data.copy()
            del form_data['id']
            instance = self.model()
            #print pk, form_data
            if pk:
                # get the related instance
                instance = self.model.objects.get(pk = pk)
            else:
                if not insert_new:
                    # skip if new and dont insert
                    continue
            # get a ModelForm based on supplied fields
            #print 1
            form = forms.getExtJsModelForm(self.model, fields_list = form_data.keys())
            #print 2
            form = form(form_data, instance = instance)
            #print 3
            forms_items.append(form)
            #print 4
            if not form.is_valid():
                print 'invalid form', form.errors
                errors.append(form.errors)
                
        if not errors:
            for form in forms_items:
             #   print 5
                form.save()
              #  print 6
            return True
        else:
            # todo : detailed errors
           # print 7
            raise Exception(errors)
                