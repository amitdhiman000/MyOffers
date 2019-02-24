// namespace App
var App = {

    Type: function(o) {
        return ((typeof(o) !== 'undefined') && (null !== o))?Object.prototype.toString.call(o).slice(8, -1):'undefined';
    },
    Bool: function(o) {
        this.Type(o) !== 'undefined';
    }
    Select: function(exp) {
        return document.querySelectorAll(exp);
    },
    On: function(objs, event, func) {
        for (obj of objs) {
            obj.addEventListener(event, func);
        }
    },
    Off: function(objs, event) {
        for (obj of objs) {
            obj.removeEventListener(event, func);
        }
    },
    Val: function(objs, val)
    {
        var valid = App.Bool(val);
        var retVal = val;
        for (obj of objs) {
            switch(obj.tagName.toLowerCase()) {
            case 'input':
            case 'select':
                var type = obj.getAttribute('type');
                switch(type) {
                case 'radio':
                case 'checkbox':
                    if (valid && (obj.checked = val));
                    retVal = obj.checked;
                    break;
                default:
                    if (valid && (obj.value = val));
                    retVal = obj.value;
                    break;
                }
            default:
                if (valid && (obj.innerHTML = val));
                retVal = obj.innerHTML;
                break;
            }
        }
        return retVal;
    },

    Engine: class {
        constructor() {
            this.components = {};
        }
        render(name) {
            this.components[name].render();
        }
    },

    History: class {

    },

    Form: class {
        constructor($form, handlers) {
            this.form = $form;
            this.handlers = handlers;
            this.form.
        }
        onSubmit(e, $form)
        {
            console.log("+AppFrom::ajaxSubmit");
            e.$form = $form;
            var action = $form.attr('action');
            console.log('action : '+ action);
    
            var handler = $form.data('data-handler');
            handler = (handler)? handler: window[$form.attr('data-delegate')];
    
            if (handler) {
                handler.before = (handler.before)? handler.before : this.before;
                handler.after = (handler.after)? handler.after: this.after;
            } else {
                handler = this;
            }
    
            if (handler.before(e) === false)
                return;
    
            $AppRequest.post(action, $form.serialize(), (status, json) => {
                e.status = status;
                e.resp = json;
                handler.after(e);
            });
        }
        before(e) {
            console.log('+AppForm::before');
            return true;
        }
        after(e) {
            console.log('+AppForm::after');
            if (e.status) {
                $AppNoti.info({title:"Successful", text:e.resp.message});
            } else {
                var errors = '';
                for (var key in e.resp.data) {
                    console.log(key + ' : '+ e.resp.data[key]);
                    errors += e.resp.data[key]+'<br />';
                }
                $AppNoti.error({title:e.resp.message, text:errors});
            }
        }
    },
};