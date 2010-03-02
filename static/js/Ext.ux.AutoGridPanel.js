
Ext.ux.AutoGridPanel = Ext.extend(Ext.grid.EditorGridPanel, {
     deferredRender :true,
     initComponent: function() {
  
        if (this.columns && (this.columns instanceof Array)) {
            this.colModel = new Ext.grid.ColumnModel(this.columns);
            delete this.columns;
        }
        // Create a empty colModel if none given
        if (!this.colModel) {
            this.colModel = new Ext.grid.ColumnModel([]);
        }
        Ext.ux.AutoGridPanel.superclass.initComponent.call(this);
        // register to the store's metachange event
        if (this.store) {
             //console.log('this.store', this.store);
           // this.store.on("load", this.onStoreLoad, this);
             this.store.on("metachange", this.onMetaChange, this);
       //     this.store.on("beforeload", function() {alert('beforeload')}, this);
        //     this.store.on("loadexception ", function() {alert('loadexception ')}, this);
       //    this.store.on("load", function() {alert('load');}, this);
            //console.log('init this.store', this.store.sortInfo);
        }
        // Store the column model to the server on change
        if (this.autoSave) {
            this.colModel.on("widthchange", this.saveColumModel, this);
            this.colModel.on("hiddenchange", this.saveColumModel, this);
            this.colModel.on("columnmoved", this.saveColumModel, this);
            this.colModel.on("columnlockchange", this.saveColumModel, this);
            this.on("columnresize", this.saveColumModel, this);
        }
        
      //  this.on("columnresize", this.saveColumModel, this);
      
        this.on("show", this.onShow, this);
 //    this.on("render", this.onRender, this);

        
    },
    // onBeforeLoad: function(store, meta) {
        // this.el.mask("Chargement...");
    // },
    // onLoad: function(store, meta) {
        // this.el.unmask();
    // },
    
    onShow:function() {
       // console.log('autogrid onShow');
    },
    
    // onRender:function() {
        // console.log('autogrid onRender');
    // },
    onMetaChange: function(store, meta) {
    //console.log("onMetaChange", meta.fields);
        // loop for every field, only add fields with a header property (modified copy from ColumnModel constructor)
        //alert('store onmetachange');
        var c;
        var config = [];
        var lookup = {};
        
 //  alert('onMetaChange');
        if (this.plugin) {
           // console.log(this.plugin);
            config[config.length] = this.plugin;
        }
        
         //for (var i = 0, len = meta.listeners.length; i < len; i++) {
           // l = meta.listeners;
           // for( var obj in l) {
                // TODO : check double metachange
                // console.log(obj);
                // console.log(l[obj]);
                 //this.on( meta.listeners);
            //}
         //}
         
        for (var i = 0, len = meta.fields.length; i < len; i++) {
            c = meta.fields[i];
   
            if (c.header !== undefined) {
                if (typeof c.dataIndex == "undefined") {
                    c.dataIndex = c.name;
                }
                if (typeof c.renderer == "string") {
                    c.renderer = Ext.util.Format[c.renderer];
                }
                if (typeof c.id == "undefined") {
                    c.id = 'c' + i;
                }
 

                c.sortable = true;
                //delete c.editor;
                config[config.length] = c;
                //config[config.length].editor = c.editor;
                lookup[c.id] = c;
            //    console.log(config);
            }
        }
        // Store new configuration
        
        //
        // Re-render grid
        //alert(this.rendered);
        
        this.getColumnModel().setConfig(config);
        
        // if remoteSort=false then dont overrride local sortInfo
        // if (!this.remoteSort) {
            // store.sortInfo = this.sortInfo
        // }
        // console.log(store.sortInfo.field, meta.sortInfo.field);
        
        if (this.rendered) {    
            
            //this.store.reader.jsonData.metaData.fields);         
            this.getView().syncFocusEl(0);
            
              var reinit_btn = this.getView().hmenu.getComponent('reset_colModel');
              if (!reinit_btn) {
                  this.getView().hmenu.add(
                        { id: "reset_colModel", text: "Réinitialiser les colonnes", cls: "xg-hmenu-reset-columns", handler:function(btn, event) {this.razColumModel();}, scope:this }
                    );
               }
               
        }
 
      
    },

    onStoreLoad : function() {
        //console.log('onStoreLoad 1');
        var view = this.getView();
        if((true === view.forceFit) || (true === this.forceFit)) {
            view.fitColumns(); 
        }
        //console.log('onStoreLoad 2');
        //alert('onStoreLoad 2');
    },
 
    razColumModel: function() {
        Ext.Ajax.request({
            url: this.saveUrl,
            params: { raz:true },
            scope:this,
            success: function() {
                this.store.reload();
            
            }
 
            
        })
    },
    
    saveColumModel: function() {
        // Get Id, width and hidden propery from every column
       // console.log('saveColumModel');
        var c, config = this.getColumnModel().config;
        var fields = [];
        for (var i = 0, len = config.length; i < len; i++) {
            c = config[i];
            fields[i] = { name: c.name, width: c.width };
            if (c.hidden) {
                fields[i].hidden = true;
            }
        }
        var sortState = this.store.getSortState();
        // Send it to server
        //console.log("save config", fields);         
        Ext.Ajax.request({
            url: this.saveUrl,
            params: { fields: Ext.encode(fields), sort: Ext.encode(sortState) }
        });
    }
});