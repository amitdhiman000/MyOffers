import {$} from '../../libs/jquery/jquery-3.3.1.min';
import {ObjectUtil} from './AppUtils';

export class UINoti {

    link: string = window.location.href;
    title: string = 'Alert';
    text: string = 'Notification';
    timeout: number = 5000;

    constructor(config: any)
    {
        ObjectUtil.Instance().merge(this, config);
    }

	show() {
        let This = this;
        let $elm = $('#wt-noti').clone().removeAttr('id');
		$elm.fadeIn({duration: 1000,
			start: function() {
				$elm.find('.wt-notititle').html(This.title);
				$elm.find('.wt-notibody').html(This.text);
				$elm.find('.wt-notilink').attr('href', This.link);
			}
		}).delay(This.timeout).fadeOut({
			duration:1000,
			always: function() { $elm.remove();}
		});
		$('.wt-notibox').append($elm);
    }
}