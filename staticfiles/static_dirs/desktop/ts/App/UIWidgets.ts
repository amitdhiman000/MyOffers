import $ from 'jquery';
import { AppUtil, ObjectUtil } from './AppUtils';
import {HttpService, HttpResponseHandler} from './HttpService';


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
    $overlay: any = null;
    $closebtn: any = null;
    $body: any = null;
    $html: any = null;
    $html_def: any = null;

    _shown: boolean = false;
    _options_def: any = { closeBtn:true, closeOnEscape:true, closeOnClickOutside:true, onClose: ()=>{} };
    _options: any = null;

    private static _instance: UIOverlay = null;

    public static Instance()
    {
        return this._instance || (this._instance = new this());
    }

    constructor() {
        this.$overlay = $('#wt-overlay');
		this.$closebtn = this.$overlay.find('.wt-closebtn');
		this.$body = this.$overlay.find('.wt-overlay-body');
		this.$html_def = $('<div style="width:80%; height:inherit; margin: 0 auto; background:#fff;" data-type="none"></div>');
		this.$html = this.$html_def;
		this.$closebtn.on('click', this, this._onclose);
		this.$overlay.on('click', this, this._onclick);
		this.$overlay.on('keyup', this, this._onKeyUp);
		this._shown = false;
		this._options = ObjectUtil.merge(this._options_def, {});
    }

	_apply_options(options: any) {
		this._options = ObjectUtil.merge(this._options_def, options);
		if (this._options['closeBtn'] === false)
			this.$closebtn.hide();
		else
			this.$closebtn.show();
    }

	shown() {
		return this._shown;
    }

	show($html=this.$html_def, options={}): this {
		this._apply_options(options);
		/* ordering matter for correct heights */
		this.$overlay.show();
		this.update($html);
		this.$overlay.focus();
		this._shown = true;
		$('body').toggleClass('ui-noscroll', this._shown);
		return this;
    }

	hide(): this {
		this.$overlay.hide();
		this._shown = false;
		$('body').toggleClass('ui-noscroll', this._shown);
		return this;
    }

	update($html: any): this {
		this.$html = $($html);
		this.$body.html(this.$html.show());
		let $scroll = this.$html.find(".wt-overlay-scroll");
		if ($scroll.exists()) {
			let h1 = this.$body.height();
			let h2 = this.$html.height();
			let h3 = $scroll.height();
			if (h1 < h2) {
				let h4 = h3 - (h2 - h1);
				console.log("h4 : "+h4);
				$scroll.height(h4);
			}
		}
		return this;
    }

	clear(): this {
		this.update(this.$html_def);
		return this;
    }

	close() {
		console.log("CLOSE OVERLAY");
		this.$closebtn.click();
    }

	_close(e: any) {

		let $html = this.$html.hide();
		if ($html.attr('data-type') == 'persist') {
			setTimeout(function(){ $html.appendTo('body'); }, 100);
		} else {
			$html.remove();
		}
		this.hide();
    }

	_onclose(e: any) {
		console.log("ONCLOSE OVERLAY");
		e.data._close(e);
    }

	_onclick(e: any) {
		console.log("ONCLICK OVERLAY");
		let This = e.data;
		if (This._options["closeOnClickOutside"] === true && $(e.target).parent().is(This.$overlay)) {
			This._close(e);
		}
    }

	_onKeyUp(e: any) {
		console.log("ONKEYUP OVERLAY");
		let This = e.data;
		if (This._options["closeOnEscape"] === true && e.keyCode == KEYS.ESCAPE) {
			This._close(e);
		}
	}
}


/* App Modal */
export class UIModal {
    show($html: any, options?: any): this {
        UIOverlay.Instance().show($html, { closeOnClickOutside:true, onClose: this.onClose});
        return this;
    }

    update($html: any): this {
        UIOverlay.Instance().update($html);
        return this;
    }

    hide(): this {
        UIOverlay.Instance().hide();
        return this;
    }

    close(): this {
        UIOverlay.Instance().close();
        return this;
    }

    onClose(e: any) {

    }
};


export class UIDialog {
    show($html: any) {
        UIOverlay.Instance().show($html);
    }

    hide() {
        UIOverlay.Instance().hide();
    }

    close() {
        UIOverlay.Instance().close();
    }
};


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


export class UIProgressBar {
    $_ui: any = null;
    constructor(title: string, btnText: string) {
        this.$_ui = `<div class="wt-progress-outer" >
                    <div class="wt-progress-inner">
                    <div class="wt-progress-filename">${title}</div>
                    <div class="wt-progress-bar">&nbsp;0%</div></div>
                    <div class="wt-progress-control">
                    <button class="ui-btn">${btnText}</button>
                    </div></div>`;
    }

    show($parent: any) {
        $parent.append(this.$_ui);
        this.$_ui.show();
    }
};

export class UIFileUpload {

    _name: string = 'UIFileUpload';
	_uploads: any = [];
    
    $_hidden: any = null;
    $_ui: any =  null;
    $_self: any = null;
    
    _overrides: any = {};
    _config: any = {maxFiles: 1, mimeType: 'image', maxSize: 1024,};

    constructor($Inst: any, overrides: any, config: any) {
        console.log('+UIFileUpload : '+$Inst.prop('tagName'));
        ObjectUtil.merge(this._overrides, overrides);
        ObjectUtil.merge(this._config, config);
        this.$_self = $Inst;
        this._create();
    }

    _create() {
        let This = this;
        console.log('+_create['+This._name+']');
        This.$_ui = $('<div class="wt-progress-div" ></div>');
        This.$_ui.css({width: This.$_self.css('width')});
        This.$_hidden = $('<input type="hidden" name="files" value="" >');
        This.$_self.before(This.$_hidden);
        This.$_self.after(This.$_ui);
        This.$_self.on('change', This._upload.bind(This));
        This.$_self.on('DOMNodeRemoved', This._destroy.bind(This));
    }
        
    _destroy(e: any) {
        console.log('+_destroy['+this._name+']');
        this.$_ui.remove();
        this.$_hidden.remove();
    }

    _upload(e: any) {
        console.log('+_upload');
        e.stopPropagation();
        e.preventDefault();
        let This = this;
        let FileField = e.target;
        let Files = $(FileField)[0].files;
        let count = This.$_ui.find('.wt-progress-outer').length;
        console.log('count : '+count);
        let rem = This._config.maxFiles - count;
        if (rem == 0) {
            FileField.value = '';
            console.log('Already attached to max limit');
            return;
        }

        if (rem > Files.length) {
            rem = Files.length;
        }
        for (let i = 0; i < rem; ++i) {
            console.log('name : '+ Files[i].name + ' data : '+Files[i]);
            This._uploadFile(Files[i]);
        }
    }
    
    _uploadFile(file: any) {
        console.log('+_uploadFile');
        let This = this;
        let formData = new FormData();
        let fileName: string = file.name;
        let csrf: any = AppUtil.csrfToken();
        for (let key in csrf) {
            formData.append(key, csrf[key]);
        }
        formData.append('image', file);
        //(fileName.length > 20 && (fileName = fileName.substring(0, 20)));

        let $item = $(`<div class="wt-progress-outer" >'
                        <div class="wt-progress-inner">'
                        <div class="wt-progress-filename">${fileName}</div>'
                        <div class="wt-progress-bar">&nbsp;0%</div></div>'
                        <div class="wt-progress-control">'
                        <button class="ui-btn">Cancel</button>'
                        </div></div>`);
        let $cancelBtn = $item.find('.ui-btn');
        $cancelBtn.on('click', This._cancel.bind(This));
        This.$_ui.append($item);

        const callbacks = {
            progress_up :(percent: number) => {
                This._progress(percent);
            },
            complete: (status: boolean, jsonObj: any) => {
                if (status) {
                    console.log("upload finished");
                    let upload_ids = jsonObj.data.upload_ids;
                    This._uploads.push(upload_ids);
                    This.$_hidden.val(This._uploads.toString());
                    $cancelBtn.data('request', null);
                    $cancelBtn.data('upload_ids', upload_ids);
                    $cancelBtn.text('Remove');
                    console.log('ids : '+This._uploads.toString());
                } else {
                    console.log('file upload failed reason : '+ JSON.stringify(jsonObj));
                    $cancelBtn.remove();
                }
            }
        };
        let handler = new HttpResponseHandler(callbacks);
        let http = new HttpService();
        http.file('/upload/file/', formData, handler);
        $cancelBtn.data('request', http);
    }
    
    _cancel(e: any) {
        console.log('+_cancel');
        e.preventDefault();
        let This = this;
        let $item = $(e.target);
        console.log($item.text());
        if ($item.text() == 'Cancel') {
            let http: HttpService = $item.data('request');
            http.abort();
            console.log('aborted');
        } else {
            let id = $item.data('upload_id');
            let index = This._uploads.indexOf(id);
            This._uploads.splice(index, 1);
            This.$_hidden.val(This._uploads);
            console.log('ids : '+This._uploads.toString());
        }
        $item.parents('.wt-progress-outer').remove();
    }
    
    _progress(progress: number) {
        console.log('progress : '+progress+'%');
        let $pgbar = this.$_ui.find('.wt-progress-bar');
        $pgbar.css({width: progress+'%'});
        $pgbar.html(progress+'%');
    }
}


export class UITabs {

    _name: string = 'UITabs';
    _total: number = 2;
    _active: any = null;
    _activeIndex: number = 0;
    _overrides: any = {'beforeLoad': (num: number) => { console.log("implement beforeLoad()"); },
                        'afterLoad': (num: number) => { console.log("implement afterLoad()"); },
                        'source': (num: number) => { console.log("implement source()"); }
                    };
    $_self: any = null;

    constructor($Inst: any, overrides: any) {
        console.log('+UITabs : '+$Inst.prop('tagName'));
        this.$_self = $Inst;
        this._create();
    }
	
    _create() {
        let This = this;
        console.log('+_create['+This._name+']');
        let $elems = This.$_self.find(".wt-switchtab-nav > li > a[rel]");
        This._total = $elems.length;
        console.log("Tabs : "+ This._total);
        This._active = $elems.eq(This._activeIndex);
        let rel = This._active.prop("rel");
        This.$_self.find(rel).show();
        $elems.on("click", function(e: any) {
            console.log("+tabClicked");
            e.preventDefault();
            let rel = This._active.prop("rel");
            This._active.removeClass("wt-switchtab-a");
            This.$_self.find(rel).hide();
            This._active = $(this);
            rel = This._active.prop("rel");
            This._active.prop("class", "wt-switchtab-a");
            This.$_self.find(rel).show();
        });
    }
};