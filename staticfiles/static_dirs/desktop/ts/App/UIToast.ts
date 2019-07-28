import $ from 'jquery';

export class UIToast {

	static show(text='Error', timeout=1800) : any {
		$('<div class="wt-toast" style="display: none;" ></div>').fadeIn({
			duration: 500,
			start: function() { $(this).text(text); },
		}).delay(timeout).fadeOut(500);
	}

	static hide(): any {
		$('.wt-toast').hide();
	}
}