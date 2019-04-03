import {$} from '../../libs/jquery/jquery-3.3.1.min';



export class ObjectUtil {
    private static _instance: ObjectUtil = null;

    public static Instance()
    {
        return this._instance || (this._instance = new this());
    }

    type(o: any) {
		return (o)?Object.prototype.toString.call(o).slice(8, -1):'undefined';
    }

	isArray(o: any) {
		return this.type(o) === 'Array';
    }

	isObject(o: any) {
		return this.type(o) === 'Object';
	}
    
	merge(a1: any, a2: any) {
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

    dump(obj: any) {
		var out:string = '';
		for (var k in obj) { out += k + ': ' + obj[k]+'; '; }
		console.log(out);
	}
}

export class AppUtil {
    private static _instance: AppUtil = null;
    private _name: string = 'App';

    public static Instance()
    {
        return this._instance || (this._instance = new this());
    }

    csrfToken() {
		var $mt = $('meta[name=csrf-token]');
		var data = {};
		data[$mt.attr("key")] = $mt.attr("content");
		return data;
    }
    
	csrfField() {
		var csrfField = "";
		var token = this.csrfToken();
		for (let key in token) {
			csrfField = '<input type="hidden" name='+key+' value='+token[key]+' />';
		}
		return csrfField;
    }
    
	name() {
		if (!this._name) {
			var $mt = $('meta[name=app-name]');
			this._name = $mt.attr("content") || "/m\\";
		}
		return this._name;
    }
}

export class Event {
    _set: any = [];
	sub(p: any) {
		console.log('+Event::sub');
		if (this._set.indexOf(p) == -1)
			this._set.push(p);
    }

	unsub(p: any) {
		console.log('Event::unsub');
		var pos = this._set.indexOf(p);
		if (pos > 1)
			this._set.splice(pos, 1);

    }

	trigger(e: any) {
		console.log('+Event::trigger');
		var ret = true;
		for (let i in this._set) {
			ret = ret && this._set[i](e);
		}
		return ret;
	}
}


export class Cookie {

    private static _instance: Cookie = null;

    public static Instance()
    {
        return this._instance || (this._instance = new this());
    }

    get(cname: string) {
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
    
    set(cname: string, cvalue: string, exdays: number) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }
    
    has(cname: string) {
        return (this.get(cname) != null);
    }
};


export class Storage {
    private static _instance: Storage = null;

    public static Instance()
    {
        return this._instance || (this._instance = new this());
    }
    get(key: string) : string {
        if (typeof(Storage) !== "undefined")
            return localStorage.getItem(key);
        return "";
    }
    
    set(key: string, val: string) {
        if (typeof(Storage) !== "undefined")
            localStorage.setItem(key, val);
    }
}

