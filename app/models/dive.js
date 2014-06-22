export default DS.Model.extend({
  creation_date: DS.attr('string'),
  creation_author: DS.attr('string'),
  modification_date: DS.attr('string'),
  modification_author: DS.attr('string')
});