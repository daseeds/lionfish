export default Ember.Route.extend(SimpleAuth.ApplicationRouteMixin, {
  actions: {
    goToNewDive: function() {
      this.transitionTo('dive.new');
    },
    goToDive: function(model) {
      this.transitionTo('dive', model);
    },
    edit: function(model) {
      this.transitionTo('dive.edit', model.copy());
    },
/*    "delete": function(model) {
      this.pouch.DELETE(model);
      model.destroy();
    },*/
    cancel: function(model) {
      model.destroy();
    }
  }
});
