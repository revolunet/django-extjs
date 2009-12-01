 
import utils

# width, dateFormat, renderer, hidden, align, type


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
        
    def to_grid(self, queryset, start = 0, limit = 0, totalcount = None, json_add = "", colModel = None):
        if not totalcount: 
            totalcount = queryset.count()
            #print 'totalcount', totalcount
        json =  """{
            "success":true
            %s
            ,"metaData":{
                "root":"rows",
                "totalProperty":"totalCount",
               "successProperty": "success",
                "sortInfo":{
                   "field": "id",
                   "direction": "DESC"
                },
                "fields":""" % json_add
        
        base_fields = self.fields
        if colModel and colModel.get('fields'):
            base_fields = []
            # width, name, hidden
            for f in colModel['fields']:
                for cf in self.fields:
                    print cf, f
                    if cf['name'] == f['name']:
                        print 'found colModel for field %s' % f['name']
                        config_field = cf
                        if f.get('width'):
                            config_field['width'] = f.get('width')
                        if f.get('hidden'):                        
                            config_field['hidden'] = f.get('hidden')
                        base_fields.append(config_field)
        
        json +=  utils.JSONserialise(base_fields)
        json += "},\n"
        if queryset:
            if limit > 0:
                #from django.core.paginator import Paginator
                #paginator = Paginator(queryset, limit)
                #queryset = paginator.page(page).object_list
                queryset = queryset[int(start):int(start) + int(limit)]
                #queryset[
            json += """"rows":\n"""
            json += '['
            fields_items = []
            for item in queryset:
                idx = 0
                field_items = []
                for field in base_fields:
                    val = getattr(item, field['name'], '')
                   # print field, val
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
                    astr = utils.JSONserialise_dict_item(field['name'], val)
                    #print 'astr', astr, field
                    field_items.append(astr)
                    #u""""%s":"%s" """ % (, val))
                    #json+= 
                    #if field != self.fields[-1]: json += ","
                    
                    idx += 1
                fields_items.append('{%s}' % ','.join(field_items))
            json += ','.join(fields_items)
            json += ']\n'
        else:
            json += '"rows":[]'
        json += """\n,"totalCount":%s""" % totalcount
        json += "}\n"
        return json 
    class Meta:
        pass

