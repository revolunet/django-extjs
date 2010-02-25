 
import utils

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
        self.model = model
        self.fields = []
        
        model_fields = self.model._meta._fields()
        
        excludes = getattr(self.Meta, 'exclude', [])
        # reorder cols if needed
        order = getattr(self.Meta, 'order', None)
        if order and len(order) > 0:
            base_fields  = []
            for field in order:
                added = False
                for f in model_fields:
                    if f.name == field:
                        added = True
                        base_fields.append(f)
                if not added:
                    base_fields.append(VirtualField(field))
        else:
            base_fields = model_fields
            
        
        for field in base_fields:
            if field.name in excludes:
                continue
            if field.__class__.__name__ == VirtualField:
                self.fields.append(self.Meta.fields_conf[field.name])
                continue
            #print field, dir(field)
            fdict = {'name':field.name, 'header': field.name}
            if field.name == 'id':
                fdict['id']='id'
            if  field.__class__.__name__ == 'DateTimeField':
                fdict['type'] = 'date'
                fdict['dateFormat'] = 'Y-m-d H:i:s'
            if  field.__class__.__name__ == 'DateField':
                fdict['type'] = 'date'
                fdict['dateFormat'] = 'Y-m-d'
            elif field.__class__.__name__ == 'IntegerField':
                fdict['type'] = 'int'
            elif field.__class__.__name__ == 'BooleanField':
                fdict['type'] = 'boolean'
            elif field.__class__.__name__ == 'DecimalField':
                fdict['type'] = 'float'
                fdict['renderer'] = 'function(v) {return (v.toFixed && v.toFixed(2) || 0);}'
            elif  field.__class__.__name__ == 'ForeignKey':
                pass
            if getattr(self.Meta, 'fields_conf', {}).has_key(field.name):
                fdict.update(self.Meta.fields_conf[field.name])
               # print fdict
            self.fields.append(fdict)
        #for field in self.model:
        #    print field
   

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
        pass

