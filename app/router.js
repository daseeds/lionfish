var Router = Ember.Router.extend(); // ensure we don't share routes between all Router instances

Router.map(function() {
  this.route('component-test');
  this.route('helper-test');
  this.route('login');
  this.resource('users', {path: '/users'});
  this.resource('user', {path: '/users/:user_id'});
  this.resource('dives', {path: '/dives'});
  this.resource('dive.new',  {path:'/dive/new'});  
  this.resource('dive', {path: '/dive/:dive_id'});
  // this.resource('posts', function() {
  //   this.route('new');
  // });
});

export default Router;
