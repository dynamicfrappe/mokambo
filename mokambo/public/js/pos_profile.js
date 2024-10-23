frappe.ui.form.on("POS Profile", { 
   
    setup:function(frm) {
        
    },
    
    refresh: function (frm) {  
        console.log(444444444444)
        frm.set_query("delivery", "delivery_table", function () {
            return {
              filters: [
                ["designation", "=", "Delivery"],
              ],
            };
          });
    },

});
  