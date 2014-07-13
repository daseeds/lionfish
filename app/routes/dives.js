export default  Ember.Route.extend({
  actions: {
    "delete": function(model) {
      this.get('controller.content').removeObject(model);
      var dive = model;
      dive.deleteRecord();
      dive.save();   
      return true;
    }
  },
  model: function() {
    return this.store.find('dive');
  },

});