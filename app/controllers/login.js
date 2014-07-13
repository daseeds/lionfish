/*var CustomAuthenticator = Ember.SimpleAuth.Authenticators.OAuth2.extend({
  serverTokenEndpoint: 'http://localhost:11080/oauth2/access_token/',

  makeRequest: function(data) {
    var requestData = Ember.$.extend(data, {
      client_id: '2bfabdedbbfbd3097b45',
      client_secret: '84231bd993665411c64607558b1422e771de3004'
    });
    return Ember.$.ajax({
      url:         this.serverTokenEndpoint,
      type:        'POST',
      data:        requestData,
      dataType:    'json',
      contentType: 'application/x-www-form-urlencoded'
    });
  }
});

var LoginController = Ember.Controller.extend(Ember.SimpleAuth.LoginControllerMixin,
 {
     authenticator: CustomAuthenticator,

     actions: {
         // display an error when logging in fails
         sessionAuthenticationFailed: function(message) {
           this.set('errorMessage', message);
         },

         // handle login success
         sessionAuthenticationSucceeded: function() {
             this.set('errorMessage', "");
             this.set('identification', "");
             this.set('password', "");
             this._super();
         }
     }
 }
);

export default LoginController;*/


export default Ember.Controller.extend(SimpleAuth.LoginControllerMixin, {
  authenticator: 'simple-auth-authenticator:oauth2-password-grant'
});