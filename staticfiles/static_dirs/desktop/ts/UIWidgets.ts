import {$} from '../../libs/jquery/jquery-3.3.1.min';
import { ObjectUtil } from './AppUtils';


var KEYS = {
	BACK: 8,
	TAB: 9,
	ENTER: 13,
	ESCAPE: 27,
	LEFT: 37,
	UP: 38,
	RIGHT: 39,
	DOWN: 40,
	DELETE: 46,
};

export class UIOverlay {
    _shown: boolean = false;
    $overlay: any = null;
    $closebtn: any = null;
    $body: any = null;
    $html: any = null;
    $html_def: any = null;
    
    _options_def: any = { closeBtn:true, closeOnEscape:true, closeOnClickOutside:true };
    _options: any = null;

	init() {
		this.$overlay = $('#wt-overlay');
		this.$closebtn = this.$overlay.find('.wt-closebtn');
		this.$body = this.$overlay.find('.wt-overlay-body');
		this.$html_def = $('<div style="width:80%; height:inherit; margin: 0 auto; background:#fff;" data-type="none"></div>');
		this.$html = this.$html_def;
		this.$closebtn.on('click', this, this._onclose);
		this.$overlay.on('click', this, this._onclick);
		this.$overlay.on('keyup', this, this._onkeyup);
		this._shown = false;
		this._options_def = { closeBtn:true, closeOnEscape:true, closeOnClickOutside:true };
		this._options = ObjectUtil.Instance().merge(this._options_def, {});
    }

	_apply_options(options: any) {
		this._options = ObjectUtil.Instance().merge(this._options_def, options);
		if (this._options['closeBtn'] === false)
			this.$closebtn.hide();
		else
			this.$closebtn.show();
    }
    
	shown() {
		return this._shown;
    }
    
	show($html=this.$html_def, options={}) {
		this._apply_options(options);
		/* ordering matter for correct heights */
		this.$overlay.show();
		this.update($html);
		this.$overlay.focus();
		this._shown = true;
		$('body').toggleClass('ui-noscroll', this._shown);
		return this;
    }

	hide() {
		this.$overlay.hide();
		this._shown = false;
		$('body').toggleClass('ui-noscroll', this._shown);
		return this;
    }

	update($html: any) {
		this.$html = $($html);
		this.$body.html(this.$html.show());
		var $scroll = this.$html.find(".wt-overlay-scroll");
		if ($scroll.exists()) {
			var h1 = this.$body.height();
			var h2 = this.$html.height();
			var h3 = $scroll.height();
			if (h1 < h2) {
				var h4 = h3 - (h2 - h1);
				console.log("h4 : "+h4);
				$scroll.height(h4);
			}
		}
		return this;
    }

	clear() {
		this.update(this.$html_def);
		return this;
    }

	close(e: any) {
		console.log("CLOSE OVERLAY");
		this.$closebtn.click();
    }

	_close(e: any) {
		var $html = this.$html.hide();
		if ($html.attr('data-type') == 'persist') {
			setTimeout(function(){ $html.appendTo('body'); }, 100);
		} else {
			$html.remove();
		}
		this.hide();
    }

	_onclose(e: any) {
		console.log("ONCLOSE OVERLAY");
		e.data._close();
    }

	_onclick(e: any) {
		console.log("ONCLICK OVERLAY");
		var This = e.data;
		if (This._options["closeOnClickOutside"] === true && $(e.target).parent().is(This.$overlay)) {
			This._close();
		}
    }

	_onkeyup(e: any) {
		console.log("ONKEYUP OVERLAY");
		var This = e.data;
		if (This._options["closeOnEscape"] === true && e.keyCode == KEYS.ESCAPE) {
			This._close();
		}
	}
}



/* App Modal */
export class UIModal extends UIOverlay {

	show($html: any) {
		super.show($html, {closeOnClickOutside:true});
    }
};



export class UIOptionList {
    _name: string = 'optionList';
	_count: number = 0;
	_selectedIndex: number = 0;
	_jsonItemsList: null;

    _config: any = { minLength: 1, delay: 0};
    _overrides: any = {};
    _scrollTimer: any =  null;

    $_self: any = null;
	$_list: any = null;
    $_selectedItem: any = null;
    
    constructor($Inst: any, config: any, overrides: any) {
        console.log('+UIOptionList : '+$Inst.prop("tagName"));
        this.$_self = $Inst;
        $Inst.optionsList = this;
        /* merge the options */
        for (let key in config) {
            this._config[key] = config[key];
        }
        this._overrides = overrides;
        this._create({});
	}

    _create(e: any) {
        let This = this;
        console.log('+_create['+This._name+']');
        This.$_list = $('<ul class="wt-search-list wt-search-list-app" >');
        This.$_list.css({width: This.$_self.css('width')});
        This.$_list.on('mouseenter', 'li', This._onitemhover.bind(This));
        This.$_list.on('click', 'li', This._onitemclick.bind(This));
        This.$_list.on('scroll', This._onlistscroll.bind(This));
        This.$_self.on("keyup", This._onkeyup.bind(This));
        This.$_self.on("keypress", This._onkeypress.bind(This));
        This.$_self.on("focus", This._onfocus.bind(This));
        This.$_self.on("blur", This._onunfocus.bind(This));
        This.$_self.after(This.$_list);
    }

    _destroy(e: any) {
        this.$_list.remove();
    }

    _onfocus(e: any) {
        console.log('+_onfocus');
        this.$_list.show();
    }

    _onunfocus(e: any) {
        this.$_list.hide();
    }

    source(key: string, respCB: any) {
        if (this._overrides.source)
            this._overrides.source(key, respCB);
        else
            console.log('implement source function');
    }

    itemCreate(item: any) {
        if (this._overrides.itemCreate)
            return this._overrides.itemCreate(item);
        return '';
    }

    onItemSelect($input: any, item: any) {
        if (this._overrides.onItemSelect)
            this._overrides.onItemSelect($input, item);
        else
            console.log('implement onItemSelect function');
    }

    onEnter($input: any, item: any) {
        if (this._overrides.onEnter)
            this._overrides.onEnter($input, item);
        else
            console.log('implement onEnter function');
    }

    _ondata(jsonItemsList: any) {
        console.log('+_ondata');
        let This = this;
        This.$_list.html('');
        This._jsonItemsList = jsonItemsList;
        This._count = jsonItemsList.length;
        This._selectedIndex = 0;
        if (This._count > 0) {
            for (let i in jsonItemsList) {
                This.$_list.append(This.itemCreate(jsonItemsList[i]));
            }
            This.$_selectedItem = This.$_list.children().eq(This._selectedIndex);
            This.$_selectedItem.addClass('wt-search-item-a');
        } else {
            This.$_list.html('<div class="wt-search-item">No search results</div>');
        }
        This.$_list.show();
    }

    _setItemSelected(newIndex: number) {
        let This = this;
        let oldIndex = This._selectedIndex;
        console.log('oldIndex : '+oldIndex + ' newIndex : '+newIndex);
        if (newIndex >= 0 && newIndex < This._count) {
            if (oldIndex != newIndex) {
                let $children = This.$_list.children();
                $children.eq(oldIndex).removeClass('wt-search-item-a');
                This.$_selectedItem = $children.eq(newIndex).addClass('wt-search-item-a');
                This._selectedIndex = newIndex;
                This._notifyItemSelected();
            }
            let itemTop = This.$_selectedItem.position().top;
            let itemHeight = This.$_selectedItem.outerHeight();
            let bodyScroll = This.$_list.scrollTop();
            let bodyHeight = This.$_list.outerHeight();

            console.log('itemTop : '+ itemTop +' itemHeight : '+ itemHeight);
            console.log('bodyScroll : '+ bodyScroll +' bodyHeight : '+ bodyHeight);
            if (itemTop < 0) {
                console.log('scrollup');
                This.$_list.scrollTop(bodyScroll + itemTop);
            } else if (itemTop + itemHeight > bodyHeight) {
                console.log('scrolldown');
                This.$_list.scrollTop(bodyScroll + itemHeight - (bodyHeight - itemTop));
            }
            This.$_list.show();
        }
    }

    _onlistscroll(e: any) {
        let This = this;
        This._scrollTimer = setTimeout(function() {
            This._scrollTimer = null;
        }, 300);
    }

    _onitemhover(e: any) {
        let This = this;
        console.log('+_onitemhover');
        if (!This._scrollTimer) {
            This._setItemSelected($(e.target).index());
        }
    }

    _onitemclick(e: any) {
        console.log('+_onitemclick');
        this._setItemSelected($(e.target).index());
    }

    _notifyItemSelected() {
        if (this._count > 0 && this._jsonItemsList) {
            this.onItemSelect(this.$_self, this._jsonItemsList[this._selectedIndex]);
        }
    }

    _onkeypress(e: any) {
        console.log('+_onkeypress : '+ e.keyCode);
        if (e.keyCode === KEYS.ENTER) {
            e.preventDefault();
            var item = (this._count > 0 && this._jsonItemsList)? this._jsonItemsList[this._selectedIndex]: null;
            this.onEnter(this.$_self, item);
            this._onunfocus(e);
        }
    }

    _onkeyup(e: any) {
        console.log('+_onkeyup');
        let This = this;
        let handled = true;
        switch(e.keyCode) {
        case KEYS.UP:
            This._setItemSelected(This._selectedIndex - 1);
            break;
        case KEYS.DOWN:
            This._setItemSelected(This._selectedIndex + 1);
            break;
        case KEYS.ENTER:
            break;
        case KEYS.LEFT:
        case KEYS.RIGHT:
            This._onfocus({});
            break;
        default:
            console.log('keycode : '+e.keyCode);
            handled = false;
        }

        if (handled) {
            e.preventDefault();
            return;
        }
        var key = This.$_self.val();
        (key.length >= This._config.minLength && This.source(key, This._ondata));
    }
}