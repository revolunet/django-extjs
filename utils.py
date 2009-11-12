
# extjs special encoder
from django.http import Http404, HttpResponse, HttpResponseRedirect


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

def JsonSuccess():
    return JsonResponse('{success:true}')
   
def JsonError(error):
    return JsonResponse('{success:false, msg:"%s"}' % JsonCleanstr(error))
    
    
def JSONserialise(obj):
    if type(obj)==type({}):
        return JSONserialise_dict(obj)
    elif type(obj)==type(True):
        return obj and "true" or "false"
    elif type(obj)==type([]):
        data = []
        for item in obj:
            data.append(JSONserialise(item))
        return "[%s]" % ",".join(data)
    elif type(obj)==type(0):
        return '%s' % obj
    elif type(obj) in [type(''), type(u'')]:
        if obj == "False": 
           return "false"
        elif obj == "True":
            return "true"
        else:
            return u'"%s"' % (JsonCleanstr(obj))
    else:
        return u'%s' % obj
    return None
    
def JSONserialise_dict(inDict):
    data=[]
    for key in inDict.keys():
        if key in ['store', 'listeners', 'fn', 'handler', 'failure', 'success']:
            val = inDict[key]
            if u'%s' % val in ['True', 'False']:
                val = str(val).lower()
        else:
            val = JSONserialise(inDict[key])
        data.append('%s:%s' % (key,val))
    data = ",".join(data)
    return "{%s}" % data
    
def JsonCleanstr(inval):
    try:
        inval = u'%s' % inval
    except:
        print "ERROR nunicoding %s" % inval
        pass
    
    return inval.replace('"','\\"').replace('\n','\\n')
    #.replace('\r','-')