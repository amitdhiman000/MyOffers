var KEY_ENTER = 13;
var KEY_LEFT = 37;
var KEY_UP = 38;
var KEY_RIGHT = 39;
var KEY_DOWN = 40;

var wsuggest = function(This, opts) {
	console.log('+wsuggest');
	console.log('element : '+This.prop("tagName"));

	this.data = {
		_ui: null,
		_count: 0,
		_jsonData: null,
		_selected_item: null,
		_selected_index: 0,
	};

	this.defaults = {
		minLength: 1,
		delay: 0,
		_create: function(e) {
			data._ui = $('<ul class="ui-search-list ui-search-list-app" >');
			data._ui.css({width: This.css('width')});
			data._count = 0;
			data._selected_item = null;
			data._selected_index = 0;
			This.after(data._ui);
			console.log('set handler');
			data._ui.on('mouseenter', 'li', function(e) {
				console.log('hover');
				var index = $(this).index();
				console.log('old selected : '+ data._selected_index);
				console.log('new selected : '+ index);
				if (data._selected_index != index) {
					data._ui.children().eq(data._selected_index).removeClass('ui-search-item-a');
					data._selected_index = index;
					data._ui.children().eq(data._selected_index).addClass('ui-search-item-a');
					if (data._jsonData) {
						defaults._itemSelect(This, data._jsonData[index]);
					}
				}
			});
		},
		_destroy: function(e) {
			data._ui.remove();
			data._ui = null;
		},
		_source: function(key, resp) {
			console.log('implement _source function');
		},
		_onfocus: function(e) {
			data._ui.show();
		},
		_onunfocus: function(e) {
			data._ui.hide();
		},
		_itemSelectCurrent: function() {
			if (data._count > 0 && data._jsonData) {
				defaults._itemSelect(This, data._jsonData[data._selected_index]);
			}
		},
		 _itemSelect: function(input, item) {
			 console.log('implement _itemSelect function');
		 },
		_itemCreate: function(item) {
			console.log('implement _itemCreate function');
			return '';
		},
		_parse: function(jsonData) {
			data._ui.html('');
			
			if (jsonData.length > 0) {
				var count = 0;
				for (i in jsonData) {
					data._ui.append(defaults._itemCreate(jsonData[i]));
					count++;
				}
				data._jsonData = jsonData;
				data._count = count;
				data._selected_index = 0;
				data._selected_item = data._ui.children().eq(data._selected_index).addClass('ui-search-item-a');
				data._ui.show();
			} else {
				data._count = 0;
				data._selected_index = 0;
				data._ui.html('<div class="ui-search-item">No search results</div>');
				data._ui.show();
			}
		},
		_handleKey: function(code) {
			console.log('key : '+ code);
			switch(code) {
			case KEY_UP:
				if (data._selected_index > 0) {
					data._ui.children().eq(data._selected_index).removeClass('ui-search-item-a');
					data._selected_index--;
					var child = data._ui.children().eq(data._selected_index).addClass('ui-search-item-a');
					var cont = data._ui;
					cont.scrollTop(child.position().top + cont.scrollTop());
					//cont.scrollTop(child.offset().top - cont.offset().top + cont.scrollTop());
					if (data._jsonData) {
						defaults._itemSelect(This, data._jsonData[data._selected_index]);
					}
				}
				return true;
			case KEY_DOWN:
				if (data._selected_index < data._count - 1) {
					data._ui.children().eq(data._selected_index).removeClass('ui-search-item-a');
					data._selected_index++;
					var child = data._ui.children().eq(data._selected_index).addClass('ui-search-item-a');
					var cont = data._ui;
					//console.log("child top : "+ child.position().top);
					//console.log("scroll top : "+ cont.scrollTop());
					cont.scrollTop(child.position().top + cont.scrollTop());
					if (data._jsonData) {
						defaults._itemSelect(data, data._jsonData[data._selected_index]);
					}
				}
				return true;
			case KEY_ENTER:
				data.defaults._onunfocus();
				return true;
			case KEY_LEFT:
			case KEY_RIGHT:
			default:
				return false;
			}
		}
	};

	var defaults = this.defaults;
	var data = this.data;

	/* merge the options */
	for (var key in opts) {
		defaults[key] = opts[key];
	}
	defaults._create();

    This.on("keyup", function(e) {
		var key = This.val();
		if (true == defaults._handleKey(e.keyCode)) {
			e.preventDefault();
			return false;
		}
		console.log('min length : '+ defaults.minLength);
		if (key.length >= defaults.minLength) {
			defaults._source(key, defaults._parse);
		}
	});
	This.on("keydown", function(e) {
		console.log('keycode : '+ e.keyCode); 
		if (e.keyCode === 10 || e.keyCode === 13) {
			e.preventDefault();
			defaults._itemSelectCurrent();
		}
	});
	This.on("focus", defaults._onfocus);
	This.on("blur", defaults._onunfocus);
};

jQuery.fn.suggestions = function(options) { new wsuggest(this, options); }
