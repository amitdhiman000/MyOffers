import {$} from '../../libs/jquery/jquery-3.3.1.min';
import {History} from './History';
import {AppUtil} from './AppUtils'


export class App {

	private static _instance: App = null;
	private _history: History = null;
	private _name: string = "App";

	private constructor()
	{
		this._history = new History();
		this.init();
	}

	public static Instance(): App {
		return this._instance || (this._instance = new this());
	}
	
	private init() {
		console.log("+App::init");
	}

	public name() {
		AppUtil.Instance().name();
	}
}
