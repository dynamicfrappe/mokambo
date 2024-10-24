frappe.ui.form.on("POS Profile", { 
   
    setup:function(frm) {
        
    },
    
    refresh: function (frm) {  
      // filter the delivery in delivery table by designation of employee
        frm.set_query("delivery", "delivery_table", function () {
            return {
              filters: [
                ["designation", "=", "Delivery"],
                ["status", "=", "Active"],  
              ],
            };
          });
    },

});
  