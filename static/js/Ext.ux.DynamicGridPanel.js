 Ext.ns('Ext.ux.grid');
 
 Ext.ux.grid.DynamicGridPanel = Ext.extend(Ext.grid.GridPanel, {
      loadMask:true
      ,stripeRows:true
      ,columnLines:true
      ,enableGrouping:false
      ,initComponent:function() {
        this.store = new Ext.data.JsonStore({
          autoDestroy:true
          ,fields:[]
          ,proxy:new Ext.data.HttpProxy({
            url:this.url
        ,   method:"POST"
          })
        });
        this.columns = [];
        this.viewConfig = {
          forceFit:true
          ,onDataChange:function() {
                this.cm.setConfig(this.ds.reader.jsonData.columns);
                this.syncFocusEl(0);
          }
        };
        Ext.ux.grid.DynamicGridPanel.superclass.initComponent.call(this);
      }
    });

    Ext.reg("DynamicGridPanel", Ext.ux.grid.DynamicGridPanel);


