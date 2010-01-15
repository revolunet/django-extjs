// dynamic load of a server side form

             
         Ext.ux.DjangoForm = Ext.extend(Ext.FormPanel, {
         
                url:null
                ,baseParamsLoad:null
                ,callback:null
                ,scope:null
                
                ,border:false
                ,custom_config:null
                ,default_config:null
                ,showButtons:true
                ,showSuccessMessage:'Formulaire bien enregistre'
                
                ,initComponent:function() {
                    if (this.showButtons) {
                        this.buttons = [
                             {name:'submit', xtype:'button', iconCls:'icon-accept', text:'enregistrer', scope:this, handler:function(args) {this.submitForm();}}
                            ,{name:'reset', xtype:'button', iconCls:'icon-cancel', text:'reset',  scope:this, handler:function(args) {this.resetForm();}}
                        ]
                        }
                        
                        this.items = {border:false, 'html':'<img style="vertical-align:middle" src="/core/static/js/ext-3.1.0/resources/images/default/shared/large-loading.gif"/>&nbsp;&nbsp;&nbsp;&nbsp;loading...'}
                    this.getDefaultButton = function(name) {
                    
                    }
                    this.gotFormCallback = function(response, options) {
                        
                         var res = Ext.decode(response.responseText);
                         this.default_config = res;

                            this.removeAll();
   
                             if (this.custom_config) {
                                // add custom form config to this formpanel
                                var newconf = this.custom_config.createDelegate(this, [this])();
                                for (var i=0;i<newconf.items.length;i++) {
                                    this.add(Ext.ComponentMgr.create(newconf.items[i]));
                                }
                                
                                // auto add hidden fields from django form if needed
                                    for (var i=0;i<this.default_config.length;i++) {
                                        if (this.default_config[i].xtype == 'hidden') {
                                           this.add(Ext.ComponentMgr.create(this.default_config[i]));
                                        }
                                    }
                                        //this.default_config = res;
                            }
                            else {
                                
                                if (this.intro) {
                                    this.add({html:this.intro, style:'padding-bottom:10px;padding-top:10px;font-size:14px', border:false});
                                }
                                if (this.startItems) {
                                    this.add(this.startItems);
                                }
                                
                              //  Ext.apply(this, this.default_config);
                                 
                                for (var i=0;i<res.length;i++) {
                                    this.add(Ext.ComponentMgr.create(res[i]));
                                }
                            }
                            //finally callback your function when ready
                           if (this.callback) {
                              this.callback.createDelegate(this.scope, [this])();
                            }
                     }
                     
                     var o = {}
                     if (this.baseParamsLoad) Ext.apply(o, this.baseParamsLoad);

                        Ext.ux.DjangoForm.superclass.initComponent.apply(this, arguments);
                         
                         this.addEvents('submitSuccess', 'submitError');
                         
                     Ext.Ajax.request({
                        url:this.url
                        ,params:o
                        ,method:'GET'
                        ,scope:this
                        ,success:this.gotFormCallback
                        ,failure:this.gotFormCallback
                    });
                    
                    
                   
                }
              ,submitSuccess:function() {
                     this.fireEvent('submitSuccess');
                     if (this.showSuccessMessage) {
                         Ext.Msg.show({
                           title:'Succes',
                           msg: this.showSuccessMessage,
                           buttons: Ext.Msg.OK,               
                           icon: Ext.MessageBox.INFO 
                        });
                   }
                }
                ,submitError:function(msg) {
                
                        this.fireEvent('submitError', msg);
                        Ext.Msg.show({
                               title:'Erreur',
                               msg: 'Impossible de valider : <br>' + msg + '<br>',
                               buttons: Ext.Msg.OK,               
                               icon: Ext.MessageBox.WARNING 
                            });
                }
                
                ,validResponse:function(form, action) {
                        for (btn in this.buttons) {
                            var butt = this.buttons[btn];
                            if (butt.name == 'submit') butt.enable();
                        }
                       if (action && action.result && action.result.success) {
                           this.submitSuccess();
                       }
                       else {
                            this.submitError(action && action.result && action.result.msg || 'erreur');
                            
                       }
                       
                }
                ,invalid:function() {
                //    console.log('invalid: ', this.getForm().getValues());
                     Ext.Msg.show({
                       title:'Erreur',
                       msg: 'Impossible de valider : formulaire invalide',
                       buttons: Ext.Msg.OK,               
                       icon: Ext.MessageBox.WARNING 
                    });
                }
                ,resetForm:function() {
                    console.log('resetForm');
                    this.getForm().reset();
                }
                
                ,submitForm:function() {
                    //console.log('submitForm');
                    if (this.getForm().isValid()) {
                        for (btn in this.buttons) {
                            if (this.buttons[btn].name == 'submit') {
                                this.buttons[btn].disable();
                                }
                        }
                        this.getForm().submit({scope:this, success:this.validResponse,failure:this.validResponse});
                    } else {
                        // console.log('invalid form!');
                         // var items = this.getForm().items.items;
                        // for (f in items) {
                            // console.log(f, items[f], items[f].isValid());
                        // }
                        this.invalid()
                        }
                   }                      
                
             });
             
             
 
             
        Ext.ux.DjangoField = function(config) {
            //  console.log(config);
          //         console.log(this);
                var items = config.django_form.default_config;
                
                for (var i=0;i<items.length;i++) {
                    if (items[i].name == config.name) {
                        
                        var bConfig = items[i];
                        // prevent infinite loop
                        
                        if (config.xtype2) {
                            config.xtype = config.xtype2
                            }
                       else {
                        delete config.xtype
                       }
                      
                        Ext.apply(bConfig, config);
                      // console.log(bConfig); 
                        
                        return Ext.ComponentMgr.create(bConfig);     
                        }
                }
        }
         
        
         
        Ext.reg("DjangoForm", Ext.ux.DjangoForm);
 
        Ext.reg("DjangoField", Ext.ux.DjangoField);
         
        
 