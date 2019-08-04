
export class UITabs {

    _name: string = 'UITabs';
    _total: number = 2;
    _active: any = null;
    _activeIndex: number = 0;
    _overrides: any = {'beforeLoad': (num: number) => { console.log("implement beforeLoad()"); },
                        'afterLoad': (num: number) => { console.log("implement afterLoad()"); },
                        'source': (num: number) => { console.log("implement source()"); }
                    };
    $_self: any = null;

    constructor($Inst: any, overrides: any) {
        console.log('+UITabs : '+$Inst.prop('tagName'));
        this.$_self = $Inst;
        this._create();
    }
	
    _create() {
        let This = this;
        console.log('+_create['+This._name+']');
        let $elems = This.$_self.find(".wt-switchtab-nav > li > a[rel]");
        This._total = $elems.length;
        console.log("Tabs : "+ This._total);
        This._active = $elems.eq(This._activeIndex);
        let rel = This._active.prop("rel");
        This.$_self.find(rel).show();
        $elems.on("click", function(e: any) {
            console.log("+tabClicked");
            e.preventDefault();
            let rel = This._active.prop("rel");
            This._active.removeClass("wt-switchtab-a");
            This.$_self.find(rel).hide();
            This._active = $(this);
            rel = This._active.prop("rel");
            This._active.prop("class", "wt-switchtab-a");
            This.$_self.find(rel).show();
        });
    }
};