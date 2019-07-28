import $ from 'jquery';
import {ObjectUtil} from './AppUtils';

export class UINoti {

    link: string = window.location.href;
    title: string = 'Alert';
    text: string = 'Notification';
	timeout: number = 5000;
	
	_html = `<div class="wt-noti" >
				<a class="wt-notilink" style="display: table;" >
				<div style="display: table-cell; width: 15%; padding: 1em; ">
					<img src="/static/images/svg/checkcircle_24_1.svg" class="ui-icon24"  />
				</div>
				<div style="display: table-cell; width: 85%; vertical-align: middle;" >
					<div class="wt-notititle" style="font-weight: bold;" >
					</div>
					<div style="border-top: 1px solid #bbb; padding: 0.2em; "></div>
					<div class="wt-notibody">
					</div>
				</div>
				</a>
			</div>`;

    constructor(config: any)
    {
        ObjectUtil.merge(this, config);
	}
	
	static make(config: any): UINoti {
		return new this(config);
	}

	show() {
        let This = this;
        let $elm = $(this._html);
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