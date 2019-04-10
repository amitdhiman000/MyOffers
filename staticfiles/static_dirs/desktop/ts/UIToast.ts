import $ from 'jquery';

export class UIToast {
	private static _instance: UIToast = null;
	
	public static Instance()
	{
		return this._instance || (this._instance = new this());
	}

	constructor()
	{}

	show(text='Error', timeout=1800) : any {
		$('.wt-toast').fadeIn({
			duration: 500,
			start: function() { $(this).text(text); },
		}).delay(timeout).fadeOut(500);
	}

	hide(): any {
		$('.wt-toast').hide();
	}
}