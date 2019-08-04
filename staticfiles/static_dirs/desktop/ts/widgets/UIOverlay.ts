import $ from 'jquery';
import { ObjectUtil } from "..";
import { KEYS } from './constants';

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