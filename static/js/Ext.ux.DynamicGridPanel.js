Ext.ux.DynamicGridPanel = Ext.extend(Ext.grid.GridPanel, {

  initComponent: function(){
    /**
     * Default configuration options.
     *
     * You are free to change the values or add/remove options.
     * The important point is to define a data store with JsonReader
     * without configuration and columns with empty array. We are going
     * to setup our reader with the metaData information returned by the server.
     * See http://extjs.com/deploy/dev/docs/?class=Ext.data.JsonReader for more
     * information how to configure your JsonReader with metaData.
     *
     * A data store with remoteSort = true displays strange behaviours such as
     * not to display arrows when you sort the data and inconsistent ASC, DESC option.
     * Any suggestions are welcome
     */
    var config = {
      viewConfig: {forceFit: true},
      enableColLock: false,
      loadMask: true,
      border: false,
      stripeRows: true,
      ds: new Ext.data.Store({
		    url: this.storeUrl,
		    reader: new Ext.data.JsonReader()
		  }),
      columns: []
    };

    Ext.apply(this, config);
    Ext.apply(this.initialConfig, config);

    Ext.ux.DynamicGridPanel.superclass.initComponent.apply(this, arguments);
  },

  onRender: function(ct, position){
    this.colModel.defaultSortable = true;

    Ext.ux.DynamicGridPanel.superclass.onRender.call(this, ct, position);

    /**
     * Grid is not masked for the first data load.
     * We are masking it while store is loading data
     */
    this.el.mask('Loading...');
    this.store.on('load', function(){
      /**
       * Thats the magic!  
       *
       * JSON data returned from server has the column definitions
       */
      if(typeof(this.store.reader.jsonData.fields) === 'object') {
	      var columns = [];

	      /**
	       * Adding RowNumberer or setting selection model as CheckboxSelectionModel
	       * We need to add them before other columns to display first
	       */
	      if(this.rowNumberer) { columns.push(new Ext.grid.RowNumberer()); }
	      if(this.checkboxSelModel) { columns.push(new Ext.grid.CheckboxSelectionModel()); }

        Ext.each(this.store.reader.jsonData.fields, function(column){
          columns.push(column);
        });

	      /**
	       * Setting column model configuration
	       */
	      this.getColumnModel().setConfig(columns);
      }
      /**
       * Unmasking grid
       */
      this.el.unmask();
    }, this);
    /**
     * And finally load the data from server!
     */
    this.store.load();
  }
});
