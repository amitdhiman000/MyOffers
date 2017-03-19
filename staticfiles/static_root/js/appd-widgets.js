$.widget( "dias.switchtab", {
    options: {
        tabs: 2,
        activeTab: null,
        content: ""
    },
    _create: function() {
        this.element.addClass("switchtab");
        var len = this.element.find('.switchtab-navbar a').length;
        console.log('tabs : '+len);
        this.options.tabs = len;
        this.options.activeTab = this.element.find('.activeswitchtab');
        this.refresh();
    },
    _setOption: function( key, value ) {
		//this.options[key] = value;
        this._super(key, value);
    },
    _setOptions: function(options) {
        this._super(options);
        this.refresh();
    },
    setTab: function() {
		console.log('setTab');
		this.element.find('.switchtab-item').hide();
		var active = this.element.find('.activeswitchtab');
		this.element.find(active.attr('rel')).show();
	},
    refresh: function() {
		this.setTab();
		var This = this;
		this.element.on('click', 'a', function(e){
			e.preventDefault();
			This.element.find('.activeswitchtab').removeClass('activeswitchtab');
			$(this).addClass('activeswitchtab');
			This.setTab();
		});
    },
    _destroy: function() {
        this.element.removeClass("switchtab").text("");
    }
});



var KEY_ENTER = 13;
var KEY_LEFT = 37;
var KEY_UP = 38;
var KEY_RIGHT = 39;
var KEY_DOWN = 40;

function suggestions(opts, This)
{
	console.log('+suggestions');
	
	console.log('element : '+This.prop("tagName"))
	var handler =  {
		minLength: 1,
		delay: 0,
		_create: function(e) {
			self._ui = $('<ul class="ui-search-list ui-search-list-app" >');
			self._ui.css({width: This.css('width')});
			self._count = 0;
			self._selected_item = null;
			self._selected_index = 0;
			This.after(self._ui);
			console.log('set handler');
			self._ui.on('mouseenter', 'li', function(e) {
				console.log('hover');
				var index = $(this).index();
				console.log('old selected : '+ self._selected_index);
				console.log('new selected : '+ index);
				if (self._selected_index != index) {
					self._ui.children().eq(self._selected_index).removeClass('ui-search-item-a');
					self._selected_index = index;
					self._ui.children().eq(self._selected_index).addClass('ui-search-item-a');
					if (self._jsonData) {
						handler._itemSelect(This, self._jsonData[index]);
					}
				}
			});
		},
		_destroy: function(e) {
			self._ui.remove();
			self._ui = null;
		},
		_source: function(key, resp) {
			console.log('implement _source function');
		},
		_onfocus: function(e) {
			self._ui.show();
		},
		_onunfocus: function(e) {
			self._ui.hide();
		},
		_itemSelectCurrent: function() {
			if (self._count > 0 && self._jsonData) {
				handler._itemSelect(This, self._jsonData[self._selected_index]);
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
			self._ui.html('');
			
			if (jsonData.length > 0) {
				var count = 0;
				for (i in jsonData) {
					self._ui.append(handler._itemCreate(jsonData[i]));
					count++;
				}
				self._jsonData = jsonData;
				self._count = count;
				self._selected_index = 0;
				self._selected_item = self._ui.children().eq(self._selected_index).addClass('ui-search-item-a');
				self._ui.show();
			} else {
				self._count = 0;
				self._selected_index = 0;
				self._ui.html('<div class="ui-search-item">No search results</div>');
				self._ui.show();
			}
		},
		_handleKey: function(code) {
			console.log('key : '+ code);
			switch(code) {
			case KEY_UP:
				if (self._selected_index > 0) {
					self._ui.children().eq(self._selected_index).removeClass('ui-search-item-a');
					self._selected_index--;
					var child = self._ui.children().eq(self._selected_index).addClass('ui-search-item-a');
					var cont = self._ui;
					cont.scrollTop(child.position().top + cont.scrollTop());
					//cont.scrollTop(child.offset().top - cont.offset().top + cont.scrollTop());
					if (self._jsonData) {
						handler._itemSelect(This, self._jsonData[self._selected_index]);
					}
				}
				return true;
			case KEY_DOWN:
				if (self._selected_index < self._count - 1) {
					self._ui.children().eq(self._selected_index).removeClass('ui-search-item-a');
					self._selected_index++;
					var child = self._ui.children().eq(self._selected_index).addClass('ui-search-item-a');
					var cont = self._ui;
					//console.log("child top : "+ child.position().top);
					//console.log("scroll top : "+ cont.scrollTop());
					cont.scrollTop(child.position().top + cont.scrollTop());
					if (self._jsonData) {
						handler._itemSelect(This, self._jsonData[self._selected_index]);
					}
				}
				return true;
			case KEY_ENTER:
				handler._onunfocus();
				return true;
			case KEY_LEFT:
			case KEY_RIGHT:
			default:
				return false;
			}
		}
	};

	/* merge the options */
	for (var key in opts) {
		handler[key] = opts[key];
	}
	
	handler._create();
    This.on("keyup", function(e) {
		var key = This.val();
		if (true == handler._handleKey(e.keyCode)) {
			e.preventDefault();
			return false;
		}
		console.log('min length : '+ handler.minLength);
		if (key.length >= handler.minLength) {
			handler._source(key, handler._parse);
		}
	}).on("keydown", function(e) {
		console.log('keycode : '+ e.keyCode); 
		if (e.keyCode === 10 || e.keyCode === 13) {
			e.preventDefault();
			handler._itemSelectCurrent();
		}
	});
	This.on("focus", handler._onfocus);
	This.on("blur", handler._onunfocus);
}

jQuery.fn.suggestions = function(options) { suggestions(options, this); }
