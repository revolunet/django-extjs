// dynamic load of a server side form

             
         Ext.ux.DjangoForm = Ext.extend(Ext.FormPanel, {
         
                url:null
                ,baseParamsLoad:null
                ,callback:null
                ,custom_config:null
                ,default_config:null
                ,showButtons:true

                
                ,initComponent:function() {
                    if (this.showButtons) {
                        this.buttons = [
                             {name:'submit', xtype:'button', iconCls:'icon-genericforms-accept', text:'enregistrer', scope:this, handler:function(args) {this.submitForm();}}
                            ,{name:'submit', xtype:'button', iconCls:'icon-genericforms-cancel', text:'reset',  scope:this, handler:function(args) {this.resetForm();}}
                        ]
                        }
                    this.getDefaultButton = function(name) {
                    
                    }
                    this.gotFormCallback = function(response, options) {
                         var res = Ext.decode(response.responseText);
                         
                         this.default_config = res;
                        
                         if (this.custom_config) {
                            // apply custom config
                            Ext.apply(this, this.custom_config());
                            // add hidden fields
                            for (var i=0;i<this.default_config.items.length;i++) {
                                if (this.default_config.items[i].xtype == 'hidden') {
                                   this.items.push(Ext.ComponentMgr.create(this.default_config.items[i]));
                                    }
                            }
                         }
                         else {
                            Ext.apply(this, this.default_config);
                         }
                     
                         Ext.ux.DjangoForm.superclass.initComponent.apply(this, arguments);
                       
                         this.callback(this);
                         this.addEvents('submitSuccess', 'submitError');
                     }
                     var o = {}
                     if (this.baseParamsLoad) Ext.apply(o, this.baseParamsLoad);
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
                     Ext.Msg.show({
                       title:'Succes',
                       msg: 'Formulaire bien enregistre',
                       buttons: Ext.Msg.OK,               
                       icon: Ext.MessageBox.INFO 
                    });
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
                       if (action && action.result && action.result.success) {
                           this.submitSuccess();
                       }
                       else {
                            this.submitError(action && action.result && action.result.msg || 'erreur');
                            
                       }
                }
                ,invalid:function() {
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
                    console.log('submitForm');
                    if (this.getForm().isValid()) {
                        this.getForm().submit({scope:this, success:this.validResponse,failure:this.validResponse});
                    } else {
                        this.invalid()
                        }
                   }                      
                
             });
             
             
 
             
        Ext.ux.DjangoField = function(config) {

                var items = config.django_form.default_config.items;
                
                for (var i=0;i<items.length;i++) {
                    if (items[i].name == config.name) {
                        
                        var bConfig = items[i];
                        // prevent infinite loop
                        delete config.xtype
                        Ext.apply(bConfig, config);
                         
                        return Ext.ComponentMgr.create(bConfig);     
                        }
                }
        }
         
        
         
        Ext.reg("DjangoForm", Ext.ux.DjangoForm);
 
        Ext.reg("DjangoField", Ext.ux.DjangoField);
         
        
 