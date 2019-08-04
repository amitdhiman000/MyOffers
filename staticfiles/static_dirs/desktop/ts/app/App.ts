import {AppUtil} from './AppUtils'
import {AppHistory} from './AppHistory';
import {AppHeader} from './AppComponents';
import { AjaxForm } from './AppForm';

export class App {
	private static _instance: App = null;
	private _history: AppHistory = null;
	private _header: AppHeader = null;
	private _name: string = "App";

	private constructor()
	{
		this._history = new AppHistory();
		this._header = new AppHeader();
		this.init();
	}

	public static Instance(): App {
		return this._instance || (this._instance = new this());
	}
	
	private init() {
		console.log("+App::init");
		$(document).on("submit", "form.ajax-form", function(e) {
			e.preventDefault();
			AjaxForm.make($(this)).submit(e);
		});
	
		$(document).on("click", ".app_vlist_exp_item > a", function(e) {
			e.preventDefault();
			$(this).parent().toggleClass("expanded");
		});
	
		$(document).on("click", function(e) {
			//e.stopPropagation();
			$(".ui-dropcontent").hide();
		});
		$(document).on("click", ".ui-dropbtn", function(e) {
			e.stopPropagation();
			$(e.target).parents(".ui-dropdown").find(".ui-dropcontent").toggle();
		});
	
		$(document).on("click", ".ui-hovermenu", function(e) {
			console.log("hovermenu clicked");
			e.preventDefault();
			e.stopPropagation();
		});
	}

	public show() {
		console.log("+App::show");
	}

	public name() {
		return AppUtil.appName();
	}
}
