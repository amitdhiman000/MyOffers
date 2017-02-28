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
