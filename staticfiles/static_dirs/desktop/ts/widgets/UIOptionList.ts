import { ObjectUtil } from "..";
import { KEYS } from "./constants";

export class UIOptionList {
    _name: string = 'UIOptionList';
	_count: number = 0;
	_selectedIndex: number = 0;
	_jsonItemsList: any = null;

    _config: any = { minLength: 1, delay: 0};
    _overrides: any = { 'source': (key:string, respCB:any) => { console.log('implement source');},
                        'itemCreate': (item: any) => { console.log('implement itemCreate'); },
                        'onItemSelect': ($input: any, item: any) => { console.log('implement onItemSelect'); },
                        'onEnter': ($input: any, item: any) => { console.log('implement onEnter'); },
                    };
    _scrollTimer: any =  null;

    $_self: any = null;
	$_list: any = null;
    $_selectedItem: any = null;
    
    constructor($Inst: any, overrides: any, config: any) {
        console.log('+UIOptionList : '+$Inst.prop("tagName"));
        this.$_self = $Inst;
        $Inst.optionsList = this;
        /* merge the options */
        ObjectUtil.merge(this._config, config);
        ObjectUtil.merge(this._overrides, overrides);
        this._create();
    }
    
    source(key: string, respCB: any) {
        if (this._overrides.source)
            this._overrides.source(key, respCB);
    }

    itemCreate(item: any) {
        if (this._overrides.itemCreate)
            return this._overrides.itemCreate(item);
        return '';
    }

    onItemSelect($input: any, item: any) {
        if (this._overrides.onItemSelect)
            this._overrides.onItemSelect($input, item);
    }

    onEnter($input: any, item: any) {
        if (this._overrides.onEnter)
            this._overrides.onEnter($input, item);
    }

    /* private methods */
    _create() {
        let This = this;
        console.log('+_create['+This._name+']');
        This.$_list = $('<ul class="wt-search-list wt-search-list-app" >');
        This.$_list.css({width: This.$_self.css('width')});
        This.$_list.on('mouseenter', 'li', This._onItemHover.bind(This));
        This.$_list.on('click', 'li', This._onItemClick.bind(This));
        This.$_list.on('scroll', This._onListScroll.bind(This));
        This.$_self.on("keyup", This._onKeyUp.bind(This));
        This.$_self.on("keypress", This._onKeyPress.bind(This));
        This.$_self.on("focus", This._onFocus.bind(This));
        This.$_self.on("blur", This._onUnfocus.bind(This));
        This.$_self.on('DOMNodeRemoved', This._destroy.bind(This));
        This.$_self.after(This.$_list);
    }

    _destroy(e: any) {
        this.$_list.remove();
    }

    _onFocus(e: any) {
        console.log('+_onFocus');
        this.$_list.show();
    }

    _onUnfocus(e: any) {
        this.$_list.hide();
    }

    _onData(jsonItemsList: any) {
        console.log('+_onData');
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

    _onListScroll(e: any) {
        let This = this;
        This._scrollTimer = setTimeout(function() {
            This._scrollTimer = null;
        }, 300);
    }

    _onItemHover(e: any) {
        let This = this;
        console.log('+_onItemHover');
        if (!This._scrollTimer) {
            This._setItemSelected($(e.target).index());
        }
    }

    _onItemClick(e: any) {
        console.log('+_onItemClick');
        this._setItemSelected($(e.target).index());
    }

    _notifyItemSelected() {
        if (this._count > 0 && this._jsonItemsList) {
            this.onItemSelect(this.$_self, this._jsonItemsList[this._selectedIndex]);
        }
    }

    _onKeyPress(e: any) {
        console.log('+_onKeyPress : '+ e.keyCode);
        if (e.keyCode === KEYS.ENTER) {
            e.preventDefault();
            let item = (this._count > 0 && this._jsonItemsList)? this._jsonItemsList[this._selectedIndex]: null;
            this.onEnter(this.$_self, item);
            this._onUnfocus(e);
        }
    }

    _onKeyUp(e: any) {
        console.log('+_onKeyUp');
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
            This._onFocus({});
            break;
        default:
            console.log('keycode : '+e.keyCode);
            handled = false;
        }

        if (handled) {
            e.preventDefault();
            return;
        }
        let key = This.$_self.val();
        (key.length >= This._config.minLength && This.source(key, This._onData.bind(This)));
    }
};