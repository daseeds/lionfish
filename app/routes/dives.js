export default  Ember.Route.extend({
  actions: {
    "delete": function(model) {
      this.get('controller.content').removeObject(model);
      return true;
    }
  },
  model: function() {
    return this.store.find('dive');
  },

});