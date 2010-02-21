/*
 * Taglist autocomplete wrapper for the Mine API, Richard Marr
 *
 * Based on jQuery Autocomplete plugin 1.1 by Jörn Zaefferer (c) 2009 Jörn Zaefferer
 * http://docs.jquery.com/Plugins/Autocomplete
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 */

/**
 * TODO:
 * - bug: handle errors on ajax
 *  - like "your are not logged in"
 * - feature: delete tags
 * - feature: let the mine api do the filtering instead of the js
 * - feature: add new tag
 * - feature: show implied tags in tagcloud
 * - feature: hide already selected tags in tagpicker
 */
;(function($) {
	
	// wrap the generic autocomplete functionality (which can be reused) with tag-list specific code
	// replace a input element with a nice tagpicker, the input element becomes a hidden one, which can just be posted
	var tagLister = new(function() {
		var that = this;
		var input;
		var hiddenInput;
		var ul;
		var tags;
		var tagRetreiver;
				
		$.extend(this, {
			init : function() {
				// "this" in this context is the element on which the tagLister is working
				var el = this;

				tags = that.extractExistingTags(el);
				that.replaceHTML(el);
				tagRetreiver = new that.TagRetreiver(that);
				that.addAutoCompleteBehaviour(input);
				return hiddenInput;
			},
			replaceHTML : function(el) {
				var attrs = {
					id      : el.attr("id"),
					name    : el.attr("name"),
					value   : tags.join(" "),
					"class" : el.attr("class"),
				}

				var i=1;
				while ($("#taglist"+i).length) {i++}
				var widgetId = "taglist"+i;

				el.replaceWith('<div class="taglist-widget" id="'+widgetId+'"><input type="hidden" id="'+attrs.id+'" name="'+attrs.name+'" value="'+attrs.value+'" /></div>');
				hiddenInput = $("#"+widgetId+" input[type=hidden]");
		
				hiddenInput.after('<input type="text" class="'+attrs.class+'"/>');
				hiddenInput.before('<ul></ul>');

				input = $("#"+widgetId+" input[type=text]");
				ul = $("#"+widgetId+" ul");

				for (var i=0; i<tags.length; i++) {
					ul.append('<li tag="'+tags[i]+'">'+tags[i]+'</li>');
				}
			},
			extractExistingTags : function(el) {
				var value = el.attr("value").trim();
				return value ? value.split(/\s+/) : [];
			},
			parseApiResult : function(data) {
				// opening the envelope
				// mapping data and value properties
				var result = [];
				for (var i=0; i<data.result.length; i++) {
					result[i] = data.result[i].tag;
					result[i].data = result[i].tagId;
					result[i].value = result[i].tagName;
				}
				return result;
			},
			addAutoCompleteBehaviour : function(input) {
				input.autocomplete(
					tagRetreiver.getTags,
					{
						minChars: 1,
						autoFill: false,
						mustMatch: false,
						cacheLength: 0,
						matchContains: true,
						scrollHeight: 220,
						formatItem: function(data, i, total, term) {
							return "<span class='tag list'>"+data.tagName+"</span> "+
								"<span class='tag cloud'>"+data.tagCloud.replace(data.tagName,'')+"</span>";
						},
						parse : this.parseApiResult
					}
				).result(function(event, data, formatted) {
					// this is all kinda hacky; wheels will fall off this wagon
					if ($.inArray(formatted, tags)==-1) {
						tags.push(formatted);
						hiddenInput.attr("value", tags.join(" "));
						ul.append('<li tag="'+formatted+'">'+formatted+'</li>');
					}
					input.attr("value", "");
				});				
			},
			filter : function() {
				return input.attr("value");
			},
			TagRetreiver : function(tagLister) {
					var completeResult = null;

					// assuming we're on the same domain, which is true for now
					var baseUrl = document.location.href.match(/[^:]+:\/\/[^\/]+/)[0];

					$.getJSON(
						baseUrl+"/api/tag.json",
						function(data) {
							completeResult = tagLister.parseApiResult(data);
						}
					);

					this.getTags = function() {
						if (!completeResult) {
							return [];
						}
						var filter = tagLister.filter();
						return $.grep(completeResult, function(entry) {
							return entry.tagName.indexOf(filter)==0;
						});
					}
				}
			}
		);	
	})();
	
	
	$.fn.extend({taglist: tagLister.init});

})(jQuery);