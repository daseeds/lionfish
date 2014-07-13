export default  Ember.Route.extend(SimpleAuth.AuthenticatedRouteMixin, {

  model: function() {
    return this.store.find('user');
  },

});