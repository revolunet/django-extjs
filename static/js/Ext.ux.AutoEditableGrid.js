    
Ext.ux.AutoEditableGrid = Ext.extend(Ext.ux.AutoGrid, {
     showToolbar:true
     ,url:''
     ,remoteSort:true
     ,sortInfo:{}
    ,initComponent:function() {
    
            this.store = new Ext.data.JsonStore({
                    autoLoad:true
                    ,baseParams:{}
                    ,remoteSort:this.remoteSort
                    ,sortInfo:this.sortInfo
                    ,proxy:new Ext.data.HttpProxy({
                        url:this.url
                        ,method:'POST'
                    })
                    ,reader: new Ext.data.JsonReader({
                        root:'rows'
                        ,id:'id'
                    })

                })
     //   console.log('initComponent AutoEditableGrid', this.sortInfo, this.store.sortInfo);
        this.GridCheckboxes = new Ext.grid.CheckboxSelectionModel();
        this.sm = this.GridCheckboxes;
	    this.plugin = this.GridCheckboxes;
 
        this.btn_new = new Ext.Button({
                        text:'add new'
                        ,iconCls:'icon-user_add'
                        ,scope:this
                        ,handler:function() {
                          this.addRow();
                        }
                        
                    });
        this.addRow = function() {
                initial = {}
                var myStore = this.getStore();
                var r = new myStore.recordType(initial, 0); 
                myStore.insert(0, r);  
                this.startEditing(0, 1);
        }
        this.btn_delete = new Ext.Button({
                        text:'delete'
                        ,iconCls:'icon-user_delete'
                        ,scope:this
                        ,handler:function() {
                            alert('del');
                            var records = this.getSelectionModel().getSelections();
                            // todo messagebox confirm
                        }
                    });
        this.btn_save = new Ext.Button({
                        text:'save'
                        ,disabled:true
                        ,iconCls:'icon-disk'
                        ,scope:this
                        ,handler:function() {
                            var modified = this.getStore().getModifiedRecords();
                            var mod = []
                           Ext.each(modified, function(item, index, all) {
                                    a = {}
                                    a.id = item.id
                                    Ext.apply(a, item.getChanges());
                                    mod.push(a);
                                },this);
                            
                            Ext.Ajax.request({
                               url: this.store.proxy.url,
                               method :'POST',
                               callback : function(options, success, response) {
                                    json  = Ext.decode(response.responseText);
                                    if (!success || !json.success) {
                                        alert("Erreur : " + json.msg);
                                    }
                                    else{
                                        this.btn_save.stopBlink();
                                        this.btn_save.disable();
                                        this.getStore().commitChanges();
                                        this.getStore().reload();
                                        }
                               },
                               scope: this,
                               params: { update: Ext.encode(mod)}
                            });
                        }
                        ,counter:0
                        ,task_blink:{
                            run: function(){
                                nclass = (this.btn_save.counter%2==0)?'icon-disk-red':'icon-disk';
                                this.btn_save.setIconClass(nclass);
                                this.btn_save.counter+=1;
                            },
                            scope:this,
                            interval: 500 
                        }
                        ,startBlink:function(e) {
                             this.enable();
                             Ext.TaskMgr.start(this.task_blink);
                        }
                        ,stopBlink:function(e) {
                            this.setIconClass('icon-disk');
                            Ext.TaskMgr.stop(this.task_blink);
                        }
                    });
                    
        if (this.showToolbar) this.tbar = [
                    this.btn_new
                    ,this.btn_delete
                    ,this.btn_save       
        ];
        
        Ext.ux.AutoEditableGrid.superclass.initComponent.apply(this, arguments);
        
        this.on('afteredit', function(e) {
            this.btn_save.startBlink();
            }, this);
    } 
 
}); 


            
Ext.reg('AutoEditableGrid', Ext.ux.AutoEditableGrid); 
