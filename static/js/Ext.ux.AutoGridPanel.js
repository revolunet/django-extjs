
Ext.ux.AutoGridPanel = Ext.extend(Ext.grid.EditorGridPanel, {
  
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
             
             this.store.on("load", this.onStoreLoad, this);
             this.store.on("metachange", this.onMetaChange, this);
              //this.store.on("beforeload", function() {this.getGridEl().mask({msg:'loading...'})}, this);
             this.store.on("loadexception ", function() {alert('loadexception ')}, this);
           //this.store.on("load", function() {this.getGridEl().unmask()}, this);
        }
        // Store the column model to the server on change
        if (this.autoSave) {
            this.colModel.on("widthchange", this.saveColumModel, this);
            this.colModel.on("hiddenchange", this.saveColumModel, this);
            this.colModel.on("columnmoved", this.saveColumModel, this);
            this.colModel.on("columnlockchange", this.saveColumModel, this);
        }

        
    },
    // onBeforeLoad: function(store, meta) {
        // this.el.mask("Chargement...");
    // },
    // onLoad: function(store, meta) {
        // this.el.unmask();
    // },
    onMetaChange: function(store, meta) {
        //console.log("onMetaChange", meta.fields);
        // loop for every field, only add fields with a header property (modified copy from ColumnModel constructor)
        //alert('store onmetachange');
        var c;
        var config = [];
        var lookup = {};
   //alert('onMetaChange');
        if (this.plugin) {
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
           // alert(c.name);
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
                if (c.editor && c.editor.isFormField) {
                    c.editor = new Ext.grid.GridEditor(c.editor);
                  //  console.log(c.editor);
                }
                c.sortable = true;
                //delete c.name;
                config[config.length] = c;
                lookup[c.id] = c;
            }
        }
        // Store new configuration
        this.colModel.config = config;
        this.colModel.lookup = lookup;
        // Re-render grid
        
        if (this.rendered) {
            this.view.refresh(true);
        }

        this.view.hmenu.add(
            { id: "reset", text: "Reset Columns", cls: "xg-hmenu-reset-columns" }
        );
    },

    onStoreLoad : function() {
        //alert('onStoreLoad 1');
        var view = this.getView();
        if((true === view.forceFit) || (true === this.forceFit)) {
            view.fitColumns(); 
        }
        //alert('onStoreLoad 2');
    },

    saveColumModel: function() {
        // Get Id, width and hidden propery from every column
        var c, config = this.colModel.config;
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