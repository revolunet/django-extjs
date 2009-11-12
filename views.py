#-*- encoding:UTF-8 -*-

#
# this is an example view to display and submit our forms
#
#
  
import datetime
from django import forms
from django.db import models
from django.http import Http404, HttpResponse, HttpResponseRedirect


# import our stuff
from django_extjs.forms import ExtJsForm
from django_extjs import utils 

TITLE_CHOICES = [['MR', 'Mr.'], ['MRS', 'Mrs.'], ['MLLE', 'Mlle.']]
       
 
#
#
# Simple Email Form Example
#
#

# here you define a standard django form
class EmailFormExample(forms.Form):
    subject = forms.CharField(max_length=100, required=True, initial="sujet...", label="mon sujet", widget = forms.TextInput(attrs={'style':'border:2px solid green', 'size':30}))
    sender = forms.EmailField(initial='test@revolunet.com')
    to = forms.EmailField(label='email to?')
    cc_myself = forms.BooleanField(required=False, initial=True)
    message = forms.CharField(initial='My example message', widget=forms.widgets.Textarea(attrs={'style':'text-align:center', 'cols':40, 'rows':10}))
    
    def __init__(self, *args, **kwargs):
        super(EmailFormExample, self).__init__(*args, **kwargs)
        # add some predefined choice to any field (renders a combo)
        self.fields['sender'].choices = (('admin@revolunet.com','admin@revolunet.com'),('test','test@revolunet.com'),('bad email','bad email')) 

# the view that handles your form
def example_email(request):
    """ 
        this view handles :
        .serving the form json config based on the django Form (EmailFormExample)
        .form result processing (POST)
    """
    
    # set the default form
    baseform = EmailFormExample
    # add our stuff
    ExtJsForm.addto(baseform)
    
    if request.method == 'POST':
        # load the form with supplied data
        form = baseform(request.POST)
        if form.is_valid(): 
            print "FORM SUBMITTED, do your custom processing, like sending the email"
            return utils.JsonSuccess()
        else:
            return utils.JsonError(form.html_errorlist())
    else:
        # init a blank form
        # you can override some default fields values
        form = baseform(initial = {'message':'the new message text'})
        
    return utils.JsonResponse(form.as_extjs())
    
    
#
#
# ModelForm Example
#
#

class AbstractModelExample(models.Model):
    name = models.CharField(max_length=100, default="blabla", verbose_name="Votre nom", blank=True)
    titre = models.CharField(choices=TITLE_CHOICES)
    phone = models.CharField(blank=True)
    phone2 = models.CharField(verbose_name="Telephone", blank=True)
    age = models.IntegerField(default=5, blank=True)
    date = models.DateField(verbose_name="Date de naissance")
    email = models.EmailField(verbose_name="Email de secours")
    tester = models.BooleanField(default=False, verbose_name="est un testeur")
    offre = models.CharField(blank = True)
    provenance = models.CharField(blank = True)
    decimal = models.FloatField(default=0, verbose_name="decimal")
    now = models.DateTimeField(verbose_name="DateTimeField")
    myid = models.IntegerField(default=1)
    
    class Meta:
        abstract = True
        

class AbstractModelExampleForm(forms.ModelForm):    
    
    # here you can add some fields that are not in the model
    subject = forms.CharField(max_length=100, required=False, initial="sujet...", label="champ hors modele")
    available = forms.BooleanField(initial=True, label="champ hors modele 2")
    pwd = forms.CharField(initial='blex', label="test password", widget = forms.widgets.PasswordInput)
    #id = forms.BooleanField(label="test")
    
    def __init__(self, *args, **kwargs):
        super(AbstractModelExampleForm, self).__init__(*args, **kwargs)
        
 
        # you change some styling options here also
        self.fields['phone2'].widget = forms.TextInput(attrs={'style':'text-align:center;font-size:16px;font-weight:bold', 'size':13})
        self.fields['offre'].widget = forms.widgets.Textarea(attrs={'style':'text-align:center', 'cols':20, 'rows':10})
         
        # bind some custom data to a select field
        self.fields['provenance'].choices = (('a','Google'),('b','Yahoo'),('c','Bing'),('d','Unknown')) 
 
        # Force client side validation
        self.fields['email'].ext = {'vtype':'email'}
        
        # set custom dates formats
        self.fields['date'].input_formats = ['%d/%m/%Y']
        self.fields['now'].input_formats = ['%d/%m/%Y %H:%M']
        
        # set instance pk for update if instance
        # if self.instance:
            # self.fields['pk'] = forms.CharField(widget=forms.widgets.HiddenInput)
            
    class Meta:
        model = AbstractModelExample
        #  fields = ['email', 'url']   # for ordering fields
        # exclude = [ 'myid']    # for hiding fields
        

def example_model(request):
    """ 
        this view handles :
        .serving the form json config based on the django ModelForm (AbstractModelForm)
        .form result processing (POST)
    """
    
    # set the default form
    baseform = AbstractModelExampleForm
    # add our stuff
    ExtJsForm.addto(baseform)
    
    if request.method == 'POST':
        # load the form with supplied data 
        form = baseform(request.POST)
        if form.is_valid(): 
            print "FORM SUBMITTED, do your custom processing, like saving the instance"
            # here you can bind an instance and update his data (doesnt work with abstract models of course)
            # form.instance = baseform._meta.model.objects.get(pk = request.POST['pk'])
            # form.save() # save instance with supplied data
            return utils.JsonSuccess()
        else:
            return utils.JsonError(form.html_errorlist())
    else:
        # init a blank form
        # you can preload the form with some model instance
        # instance = baseform._meta.model.objects.get(pk = request.GET['pk'])
        # or preload the form.inital dict
        instance = None
        initial = {'offre':'test offre !!'}
        form = baseform(instance = instance, initial = initial)
    return utils.JsonResponse(form.as_extjs())
      
    
        