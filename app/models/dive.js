export default DS.Model.extend({
	creation_date: DS.attr('string'),
	creation_author: DS.attr('string'),
	modification_date: DS.attr('string'),
	modification_author: DS.attr('string'),
	max_depth: DS.attr('string'),
	avg_depth: DS.attr('string'),
	dive_date: DS.attr('string'),
	dive_duration: DS.attr('string'),
	dive_coordinates: DS.attr('string'),
});