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
 * - feature: let the mine api do the filtering instead of the js
 * - feature: hide already selected tags in tagpicker
 *  - basic version DONE; tagsyntax aware version TODO
 * - feature: should also load implied tags for the existing tags
 * - feature: show separate cloud for "recently used tags" which can be selected
 * - feature: show separate cloud for "recommended tags" which can be selected; 
 *            these are tags which are frequently used in combination with the already added tags
 * - bug: in Opera when "shoes" is en existing tag typing "sh" RETURN adds two tags "sh" and "shoes"
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
				
		var KEY = {
			UP: 38,
			DOWN: 40,
			DEL: 46,
			TAB: 9,
			RETURN: 13,
			ESC: 27,
			COMMA: 188,
			PAGEUP: 33,
			PAGEDOWN: 34,
			BACKSPACE: 8
		};
		
		var TAGSYNTAX = {
			NONE    : "",
			FOR     : "for",
			IMPLIES : "implies",
			INVALID : "invalid",
			NEWTAG  : "$$newtag$$"
		};
		
				
		$.extend(this, {
			init : function() {
				// "this" in this context is the element on which the tagLister is working
				var el = this;

				tags = that.extractExistingTags(el);
				that.replaceHTML(el);
				tagRetreiver = new that.TagRetreiver(that);
				that.addAutoCompleteBehaviour(input);
				that.addKeyDownBehaviour(input);
				that.addKeyRemoveTagBehaviour(ul);
				return hiddenInput;
			},
			replaceHTML : function(el) {
				var attrs = {
					id      : el.attr("id"),
					name    : el.attr("name"),
					value   : tags.join(" "),
					"class" : el.attr("class"),
					size    : el.attr('size')
				}

				var i=1;
				while ($("#taglist"+i).length) {i++}
				var widgetId = "taglist"+i;

				el.replaceWith('<div class="taglist-widget" id="'+widgetId+'"><input type="hidden" id="'+attrs.id+'" name="'+attrs.name+'" value="'+attrs.value+'" /></div>');
				hiddenInput = $("#"+widgetId+" input[type=hidden]");
		
				hiddenInput.after('<input type="text" class="'+attrs["class"]+'" size="'+attrs.size+'"/>');
				hiddenInput.before('<ul></ul>');

				input = $("#"+widgetId+" input[type=text]");
				ul = $("#"+widgetId+" ul");

				for (var i=0; i<tags.length; i++) {
					that.insertTagLi(tags[i]);
				}
			},
			extractExistingTags : function(el) {
				return that.splitTagString(el.attr("value"));
			},
			parseApiResult : function(data) {
				// opening the envelope
				// mapping data and value properties
				var result = [];
				for (var i=0; i<data.result.length; i++) {
					result[i] = data.result[i].tag;
					result[i].data = result[i].tagName;
					result[i].value = that.splitTagString(result[i].tagImplies)
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
								(data.tagImplies && data.tagImplies!=TAGSYNTAX.NEWTAG ? "<span class='tag cloud'> &lt; "+data.tagImplies+"</span>" : "");
						},
						parse : this.parseApiResult
					}
				).result(function(event, tag, implied) {
					that.addTag(tag, implied);
					that.clearInput();
				});				
			},
			clearInput : function(){
				input.attr("value", "");
			},
			insertTagLi : function(name, implied) {
				var className = that.hasTagSyntax(name);
				var implyHtml = "";
				name = name.replace('<', '&lt;');
				
				if (implied && implied.length) {
					className = TAGSYNTAX.IMPLIES;
					implyHtml = '<span> &lt; '+implied.join(' ')+'</span>';
				}
				ul.append('<li class="'+className+'" tag="'+name+'">'+name+implyHtml+' <span class="remove" title="remove">X</span></li>')
			},
			filter : function() {
				return input.attr("value");
			},
			splitTagString : function(string) {
				return $.grep((string||"").split(/\s+/), function(s){return s!=""});
			},
			addKeyDownBehaviour : function(el) {
				el.bind("keydown", function(event) {
					switch(event.keyCode) {
						case KEY.RETURN:
							event.preventDefault();
							
							var filter = that.filter();
							if(filter && that.hasTagSyntax(filter)!=TAGSYNTAX.INVALID) {
								that.addTag(filter);
								that.clearInput();
							}
							return false;
							break;
					}
				}).bind("keyup", function(event) {
					that.colorIfSpecialSyntax();
					that.markCurrentTag();
				})
			},
			addKeyRemoveTagBehaviour : function(ul) {
				ul.click(function(e) {
					var el = $(e.target); 
					if(el.hasClass("remove")) {
						that.removeTag(el.closest("li").attr("tag"));
					}
				})
			},
			colorIfSpecialSyntax : function() {
				input.removeClass("for implies invalid");
				input.addClass(that.hasTagSyntax(that.filter()));
			},
			markCurrentTag : function() {
				if (that.currentTagMarked) {
					ul.find("li.current").removeClass("current");
					that.currentTagMarked = false;
				}
				
				var filter = that.filter().replace(/\s+/, '');
				if ($.inArray(filter, tags)!=-1) {
					ul.find("li[tag="+filter+"]").addClass("current");
					that.currentTagMarked = true;
				}
			},
			hasTagSyntax : function (tag) {
				if (tag.match(/^[a-zA-Z-0-9_]* *$/)) {
					return TAGSYNTAX.NONE
				} else if (tag.match(/^for *: *[a-zA-Z-0-9_]* *$/)) {
					return TAGSYNTAX.FOR
				} else if (tag.match(/^[a-zA-Z-0-9_]+ *< *[a-zA-Z-0-9_]* *$/)) {
					return TAGSYNTAX.IMPLIES
				} else {
					return TAGSYNTAX.INVALID
				}
			},
			addTag : function(name, implied) {
				name = (name && name.replace(/\s+/, '')) || "";
				
				if (implied==TAGSYNTAX.NEWTAG) {
					// auch this is ugly :'(
					name = name.match(/"([^]+)"/)[1];
					implied = null;
				}
				
				if ($.inArray(name, tags)==-1) {
					tags.push(name);
					hiddenInput.attr("value", tags.join(" "));
					that.insertTagLi(name, implied);
				}
			},
			removeTag : function(name) {
				ul.find("li[tag="+name+"]").remove();
				tags = $.grep(tags, function(t){return t!=name});
				hiddenInput.attr("value", tags.join(" "));
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
						var result = []
						var filter = tagLister.filter();
						var tagFound = false;
						// filter all results, mineapi should do this in the future
						if (completeResult) {
							result = $.grep(completeResult, function(entry) {
								if (entry.tagName == filter) {
									tagFound = true;
								}
								// ignore if it doesn't match
								if (entry.tagName.indexOf(filter)!=0) {
									return false;
								}
								// ignore already selected tags
								// console.log(tags, entry.tagName)
								if ($.inArray(entry.tagName, tags)!=-1) {
									return false;
								}
								return true;
							});
						}
						// add 'create tag' entry at the bottom
						filter = filter.replace(/\s+/, '');
						if (!tagFound && $.inArray(filter, tags)==-1) {
							result.push({
								tagImplies : '$$newtag$$',
								value      : '$$newtag$$',
								tagName    : 'create tag "'+filter+'"',
								data       : 'create tag "'+filter+'"'
							})
						}
						return result;
					}
				}
			}
		);	
	})();
	
	
	$.fn.extend({taglist: tagLister.init});

})(jQuery);