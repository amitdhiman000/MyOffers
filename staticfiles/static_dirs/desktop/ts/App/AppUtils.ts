import $ from 'jquery';

export class ObjectUtil {

    static type(o: any) {
		return (o)?Object.prototype.toString.call(o).slice(8, -1):'undefined';
    }

	static isArray(o: any) {
		return this.type(o) === 'Array';
    }

	static isObject(o: any) {
		return this.type(o) === 'Object';
	}
    
	static merge(a1: any, a2: any) {
		var res = a1;
		for (var k in a2) {
			if (a2.hasOwnProperty(k)) {
				if (typeof a2[k] === 'object') {
					if (this.isArray(a2[k]))
						res[k] = [];
					else if (this.isObject(a2[k]))
						res[k] = {};
					res[k] = this.merge(res[k], a2[k]);
				} else {
					res[k] = a2[k];
				}
			}
		}
		return res;
    }

    static dump(obj: any) {
		var out:string = '';
		for (var k in obj) { out += k + ': ' + obj[k]+'; '; }
		console.log(out);
	}
}

export class AppUtil {
    private static _name: string = '';

    static csrfToken(): any {
		var $mt = $('meta[name=csrf-token]');
		var data = {};
		data[$mt.attr("key")] = $mt.attr("content");
		return data;
    }
    
	static csrfField(): string {
		var csrfField = "";
		var token = this.csrfToken();
		for (let key in token) {
			csrfField = '<input type="hidden" name='+key+' value='+token[key]+' />';
		}
		return csrfField;
    }
    
	static appName(): string {
		if (this._name == '') {
			var $mt = $('meta[name=app-name]');
			this._name = $mt.attr("content") || "/m\\";
		}
		return this._name;
    }
};

export class FormUtil {

	static setValByName($form: any, name: string, val: string) {
		console.log('+FormUtil::setValByName');
		let viewVal = val;
		let $editNode = $form.find('.ui-input[name='+name+']');
		let $viewNode = $form.find('[data-rel='+name+']');
		if ($editNode.exists()) {
			viewVal = this.setVal($editNode, val);
			$editNode.attr('data-value', val);
		}
		($viewNode.exists() && $viewNode.html(viewVal));
    }
    
	static setVal($node: any, val: string) {
        console.log("+FormUtil::setVal");
		let retVal = val;
		switch($node.prop("tagName").toLowerCase()) {
			case 'input':
				var type = $node.prop('type').toLowerCase();
				switch(type) {
					case 'text':
					case 'hidden':
						$node.val(val);
						break;
					case 'password':
						$node.val('');
						break;
					case 'radio':
					case 'checkbox':
						if (val) {
							$node.prop('checked', true);
						} else {
							$node.removeProp('checked');
						}
						retVal = $node.val();
						break;
				}
				break;
			case 'select':
				retVal = $node.find('[value='+val+']').prop('selected', true).text();
				break;
			case 'textarea':
			default:
				$node.html(val);
				break;
		}
		console.log('retVal : '+ retVal);
		return retVal;
    }
    
	static resetVal($form: any) {
        console.log("+FormUtil::resetVal");
		let This = this;
		$form.find('input[type=text], select, textarea').each(function(index: number, node: any) {
			This.setVal($(node), $(node).attr('data-value'));
		});
    }
    
	static fillByName($form: any, vals: any) {
        console.log("+FormUtil::fillByName");
		for (let key in vals) {
			let $node = $form.find('[name='+key+']');
			this.setVal($node, vals[key]);
		}
	}
};

export class AppEvent {
	_name: string = "AppEvent"
	_set: any = [];
	constructor(name?: string) {
		if (name !== undefined) {
			this._name = name;
		}
	}
	sub(p: any) {
		console.log('+AppEvent::sub');
		if (this._set.indexOf(p) == -1)
			this._set.push(p);
    }

	unsub(p: any) {
		console.log('AppEvent::unsub');
		let pos = this._set.indexOf(p);
		if (pos > 1)
			this._set.splice(pos, 1);
    }

	trigger(e: any, data: any) {
		console.log('+AppEvent::trigger');
		let ret = true;
		for (let i in this._set) {
			let val = this._set[i](e, data);
			ret = ret && val;
		}
		return ret;
	}
}

export class AppGeo {

	static locate(OnLocate: any) {
		console.log("+AppGeo::locate");
		navigator.geolocation.getCurrentPosition((pos: any) => {
			let lat: number = pos.coords.latitude.toFixed(8);
			let lng: number = pos.coords.longitude.toFixed(8);
			let ts = pos.timestamp;
			let acc = pos.coords.accuracy;
			OnLocate(lat, lng);
		}, ()=> {
            console.log("Failed to get location");
            OnLocate();
        });
	}
};

export class AppCookie {

	static get(cname: string) {
        var cv = null;
        if (document.cookie != 'undefined' && document.cookie !== '') {
            var cks = document.cookie.split(';');
            for (var i = 0; i < cks.length; i++) {
                var c = cks[i].trim();
                /* Does this cookie string begin with the name we want? */
                if (c.substring(0, cname.length + 1) === (name + '=')) {
                    cv = decodeURIComponent(c.substring(cname.length + 1));
                    break;
                }
            }
        }
        return cv;
    }
    
    static set(cname: string, cvalue: string, exdays: number) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }
    
    static has(cname: string) {
        return (this.get(cname) != null);
    }
};


export class AppStorage {

    static get(key: string) : string {
        if (typeof(Storage) !== "undefined")
            return localStorage.getItem(key);
        return "";
    }
    
    static set(key: string, val: string) {
        if (typeof(Storage) !== "undefined")
            localStorage.setItem(key, val);
    }
}

