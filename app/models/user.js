export default DS.Model.extend({
  creation_date: DS.attr('string'),
  creation_author: DS.attr('string'),
  modification_date: DS.attr('string'),
  modification_author: DS.attr('string'),
  avatar: DS.attr('string'),
  email: DS.attr('string'),
  certification: DS.attr('string'),
  level: DS.attr('string')
});