  // define the login route that defines the authentication actions
  export default   Ember.Route.extend({
    actions: {
          // action to trigger authentication with Facebook
          authenticateWithFacebook: function() {
            this.get('session').authenticate('authenticator:facebook', {});
          },
          // action to trigger authentication with Google+
          authenticateWithGooglePlus: function() {
            this.get('session').authenticate('authenticator:googleplus', {});
          }
        }
      });