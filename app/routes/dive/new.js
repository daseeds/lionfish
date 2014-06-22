import Dive from 'appkit/models/dive';

export default Ember.Route.extend({
  actions: {
    create: function(model) {
			var that = this;
      model.save();
      //.then(function(){
				this.transitionTo('dives');
			
    },
    cancel: function(model) {
      model.deleteRecord();
      this.transitionTo('dives');
      return true;
    }
  },
  model: function() {
    // provide a new photo to the template
    return this.store.createRecord('dive', {});
  }
});

