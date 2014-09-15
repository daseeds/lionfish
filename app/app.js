import Resolver from 'ember/resolver';
import loadInitializers from 'ember/load-initializers';

// setup Facebook SDK
FB.init({ appId: '631252926924840' });

// setup Google+ API
function googleApiLoaded() {
	gapi.client.setApiKey('AIzaSyAHSyCorMvWcCvBKidHERFyvSgZDFgvItU');
}

Ember.Application.initializer({
	name: 'authentication',
	before: 'simple-auth',
	initialize: function(container, application) {
		// register the Facebook and Google+ authenticators so the session can find them
		container.register('authenticator:facebook', App.FacebookAuthenticator);
		container.register('authenticator:googleplus', App.GooglePlusAuthenticator);
	}
});

var App = Ember.Application.extend({
  modulePrefix: 'appkit', // TODO: loaded via config
  Resolver: Resolver
});

loadInitializers(App, 'appkit');

// the custom authenticator that initiates the authentication process with Facebook
App.FacebookAuthenticator = SimpleAuth.Authenticators.Base.extend({
restore: function(properties) {
  return new Ember.RSVP.Promise(function(resolve, reject) {
    if (!Ember.isEmpty(properties.accessToken)) {
      resolve(properties);
    } else {
      reject();
    }
  });
},
authenticate: function() {
  return new Ember.RSVP.Promise(function(resolve, reject) {
    FB.getLoginStatus(function(fbResponse) {
      if (fbResponse.status === 'connected') {
        Ember.run(function() {
          resolve({ accessToken: fbResponse.authResponse.accessToken });
        });
      } else if (fbResponse.status === 'not_authorized') {
        reject();
      } else {
        FB.login(function(fbResponse) {
          if (fbResponse.authResponse) {
            Ember.run(function() {
              resolve({ accessToken: fbResponse.authResponse.accessToken });
            });
          } else {
            reject();
          }
        });
      }
    });
  });
},
invalidate: function() {
  return new Ember.RSVP.Promise(function(resolve, reject) {
    FB.logout(function(response) {
      Ember.run(resolve);
    });
  });
}
});

// the custom authenticator that initiates the authentication process with Google+
App.GooglePlusAuthenticator = SimpleAuth.Authenticators.Base.extend({
	restore: function(properties) {
		return new Ember.RSVP.Promise(function(resolve, reject) {
			if (!Ember.isEmpty(properties.access_token)) {
				resolve(properties);
			} else {
				reject();
			}
		});
	},
    get_email: function(access_token) {
        // Call the google api with our token to get the user info
        return new Ember.RSVP.Promise(function(resolve, reject) {
            Ember.$.ajax({
                url:         'https://www.googleapis.com/oauth2/v2/userinfo?access_token='+access_token,
                type:        'GET',
                contentType: 'application/json'
            }).then(function(response) {
                resolve (response);
            }, function(xhr, status, error) {
                console.log(error);
                reject(error);
            });
        });
    },	
	authenticate: function() {
		var _this = this;
		return new Ember.RSVP.Promise(function(resolve, reject) {
			gapi.auth.authorize({
				client_id:        '954204832191-f0rhrp1va6i2mhgg6u1i0n0sipuao7pt.apps.googleusercontent.com',
				scope:            ['openid', 'email'],
				/*redirect_uri:     'http://logmydive-dev.appspot.com/oauth2callback',*/
				'approvalprompt': 'force',
				immediate:        false
			}, function(authResult) {
				if (authResult && !authResult.error) {
					resolve({ access_token: authResult.access_token });
					var token = authResult.access_token;
                // Get all the user info
                _this.get_email(token).then(
                   function(resp) {
                       resolve({ token: token,
                                userEmail: resp.email,
                                userFn: resp.given_name,
                                userLn: resp.family_name,
                                userPic: resp.picture,
                                userGender: resp.gender,
                       });
                       console.log(userEmail)
                   },
                   function(rej) {
                       reject(rej);
                   }
               );					

				} else {
					reject((authResult || {}).error);
				}
			});
		});
	},
	invalidate: function() {
		return Ember.RSVP.resolve();
	}
});

export default App;
