import datetime
import pickle

# extjs special encoder
from django.http import Http404, HttpResponse, HttpResponseRedirect


def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365*24*60*60  #one year
    else:
        max_age = days_expire*24*60*60 
        
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)
    return response
    
def set_pickle_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365*24*60*60  #one year
    else:
        max_age = days_expire*24*60*60 
    value = pickle.dumps(value)
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)
    return response  
    
    return pickle.loads(value) 
    
def get_pickle_cookie(request, key):
    value = request.COOKIES.get(key)
    if value:
        try:
            value = pickle.loads(value) 
        except:
            print ' * ERROR unpickling cookie %s' % key
            value = None
    return value
    
def get_cookie(request, key):
    return request.COOKIES.get(key)

def datetimeFromExtDateField(indatestr):

    if indatestr.count("T")>0:
        (date, time) = indatestr.split("T")
        (an, mois, jour) = date.split('-')
        (h, m, s) = time.split(':')
        return datetime.datetime(int(an), int(mois), int(jour), int(h), int(m), int(s))
    elif indatestr.count("/") == '2':
        if indatestr.count(' ')>0:
            (date, time) = indatestr.split(" ")
            (jour, mois, an) = date.split('/')
            (h, m, s) = time.split(':')
            return datetime.datetime(int(an), int(mois), int(jour), int(h), int(m), int(s))
        else:
            (jour, mois, an) = date.split('/')
            return datetime.date(int(an), int(mois), int(jour))
    return None
     
    
def DateFormatConverter(to_extjs = None, to_python = None):
    """ convert date formats between ext and python """
    f = {}
    f['a'] = 'D'
    f['A'] = 'l'
    f['b'] = 'M'
    f['B'] = 'F'
    #f['c'] = 
    f['d'] = 'd'
    f['H'] = 'H'
    f['I'] = 'h'
    f['j'] = 'z'
    f['m'] = 'm'
    f['M'] = 'i'
    f['p'] = 'A'
    f['S'] = 's'
    f['U'] = 'W'
    #f['w'] = 
    f['W'] = 'W'
    #f['x'] = 
    #f['X'] =
    f['y'] = 'y'
    f['Y'] = 'Y'
    f['Z'] = 'T'
    out = ''
    if to_extjs:
        for char in to_extjs.replace('%',''):
            out += f.get(char, char)
    elif to_python:
        for char in to_python:
            if char in f.values():
                key = [key for key, val in f.items() if f[key] == char][0]
                out += '%%%s' % key
            else:
                out += char
            
    return out
    


def JsonResponse(contents, status=200):
    return HttpResponse(contents, mimetype='text/javascript', status=status)

def JsonSuccess(params = {}):
    d = {"success":True}
    d.update(params)
    return JsonResponse(JSONserialise(d))
   
def JsonError(error = ''):
    return JsonResponse('{"success":false, "msg":%s}' % JSONserialise(error))
    
    
def JSONserialise(obj, sep = '"', escapeStrings = True):
    import decimal
    from django.db import models
    
    if type(obj)==type({}):
        return JSONserialise_dict(obj)
    elif type(obj)==type(True):
        return obj and "true" or "false"
    elif type(obj) in [type([]), type((1,2))]:
        # if len(obj) > 50:
            # print '*********', 'list', len(obj), type(obj)
        return "[%s]" % ','.join(map(JSONserialise, obj))
        # data = []
        # for item in obj:
            # data.append(JSONserialise(item))
        # return "[%s]" % ",".join(data)
    elif type(obj) in [type(0), type(0.0), long, decimal.Decimal]:
        return '%s' % obj
    elif type(obj) in [datetime.datetime , datetime.date]:
         return u'%s%s%s' % (sep, obj, sep)
         
    elif type(obj) in [type(''), type(u'')] or isinstance(obj, models.Model):
        #print obj, isinstance(obj, str), isinstance(obj, unicode)
        if obj == "False": 
           return "false"
        elif obj == "True":
            return "true"
        else:
            if escapeStrings:
                return u'%s%s%s' % (sep, JsonCleanstr(obj), sep)
            else:
                return u'%s%s%s' % (sep, obj, sep)
    elif not obj:   
        return u'%s%s' % (sep, sep)
    else:   
        
        print 'JSONserialise unknown type', obj, type(obj), obj.__class__.__name__, isinstance(obj, models.Model)
        return u'%s' % obj
    return None
    
def JSONserialise_dict_item(key, value, sep = '"'):
    # quote the value except for ExtJs keywords
    
    if key in ['renderer', 'editor', 'hidden', 'sortable', 'sortInfo', 'listeners', 'view', 'failure', 'success','scope', 'fn','store','handler']:
        if u'%s' % value in ['True', 'False']:
            value = str(value).lower()
        else:
            # dont escape strings inside these special values (eg; store data)
            value = JSONserialise(value, sep='', escapeStrings = False)
        return '"%s":%s' % (key, value)
    else:
        value = JSONserialise(value, sep)
        return '"%s":%s' % (key, value)
     
def JSONserialise_dict(inDict):
    data=[]
    for key in inDict.keys():
        # skip quotes for ExtJs reserved names  
        data.append(JSONserialise_dict_item(key, inDict[key]))
        #if key in ['store', 'listeners', 'fn', 'handler', 'failure', 'success', 'scope']:
        #    val = inDict[key]
        #    if u'%s' % val in ['True', 'False']:
        #        val = str(val).lower()
        #else:
        #    val = JSONserialise(inDict[key])
        #data.append('%s:%s' % (key,val))
    data = ",".join(data)
    return "{%s}" % data
    
def JsonCleanstr(inval):
    try:
        inval = u'%s' % inval
    except:
        print "ERROR nunicoding %s" % inval
        pass
    
    return inval.replace('"','\\"').replace('\n','\\n').replace('\r','')
    #.replace('\r','-')