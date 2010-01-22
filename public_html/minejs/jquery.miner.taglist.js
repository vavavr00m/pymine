/*
 * Taglist autocomplete wrapper for the Mine API, Richard Marr
 *
 * Based on jQuery Autocomplete plugin 1.1 by Jörn Zaefferer (c) 2009 Jörn Zaefferer
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 */

;(function($) {
	
	// wrap the generic autocomplete functionality (which can be reused) with tag-list specific code
	$.fn.extend({
		taglist: function() {
		
			return this.css("background","#eee").autocomplete( getTagListData, {
				minChars: 1,
				autoFill: false,
				mustMatch: false,
				cacheLength: 0,
				matchContains: true,
				scrollHeight: 220,
				formatItem: function(data, i, total, term) {
					return "<span class='tag list'>"+data.tagName+"</span> "+
						"<span class='tag cloud'>"+data.tagCloud.replace(data.tagName,'')+"</span>";
				}
			});
		}
	});

})(jQuery);