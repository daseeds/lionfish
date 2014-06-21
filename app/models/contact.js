export default DS.Model.extend({
  first: DS.attr('string'),
  last: DS.attr('string'),
  avatar: DS.attr('string'),
  github: DS.attr('string'),
  twitter: DS.attr('string'),
  notes: DS.attr('string')
});