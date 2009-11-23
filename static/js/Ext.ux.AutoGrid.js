    
Ext.ux.AutoGrid = Ext.extend(Ext.ux.AutoGridPanel, {
     showBbar:false
    ,stripeRows:true
 
    ,initComponent:function() {
        this.pagesize = this.pagesize || 10;
        
        if (this.showBbar) this.bbar = new Ext.PagingToolbar({
                pageSize: this.pagesize,
                store:  this.store,
                displayInfo: true,
                displayMsg: '{0} à {1} sur {2}',
                emptyMsg: "Aucun élément à afficher"
        });
        
        var config = {  
            store:  this.store
            ,stripeRows: true
            ,loadMask: true
            ,autoSave: false
        };
        Ext.apply(this.initialConfig, config);
        Ext.ux.AutoGrid.superclass.initComponent.apply(this, arguments);

    } 

 
}); 


            
Ext.reg('AutoGrid', Ext.ux.AutoGrid); 
