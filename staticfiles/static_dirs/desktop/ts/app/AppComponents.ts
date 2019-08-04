
import $ from 'jquery';
import {ObjectUtil} from './AppUtils';
import {HttpService} from './HttpService';

export class AppNavbar {
    _config: any = {'navbar_btn': '#navbar_btn'};
    constructor(config?: any) {
        ObjectUtil.merge(this._config, config);
        $(this._config['navbar_btn']).on('click', this._onNavClicked.bind(this));
    }

    _onNavClicked(e: any) {
        console.log("+AppNavBar::_onNavClicked");
        let appleft = document.getElementById("app_leftnav");
        let apppage = document.getElementById("app_page");
        if (appleft && apppage) {
            console.log("marginLeft: "+appleft.style.marginLeft);
            if (appleft.style.marginLeft !== "-20%") {
                appleft.style.marginLeft = "-20%";
                apppage.style.width = "95%";
                apppage.style.margin = "0 auto";
            } else {
                appleft.style.marginLeft = "0";
                apppage.style.marginLeft = "20%";
                apppage.style.width = "80%";
            }
        }
    }
};

export class AppSearchbar {
    constructor(selector: any = "#app_search_input") {
        $(selector).OptionList({
            'source': this.source,
            'itemCreate': this.itemCreate,
            'onItemSelect': this.onItemSelect,
            'onEnter': this.onEnter,
        }, {minLength: 2,});
    }

    source(key: string, respCB: any) {
        let http = new HttpService();
        http.post('/search/offer/', {'key': key}, (status: any, json: any) => {
            if (true == status) {
                respCB(json.data);
            } else {
                console.log('data : '+JSON.stringify(json.data));
            }
        });
    }

    itemCreate(item: any) {
        let $item = `<li>
                        <div class="wt-search-item">
                            <a style="display:block; padding: 0.5em;" href="${item.url}"> ${item.name}</a>
                        </div>
                    </li>`;
        return $item;
    }

    onItemSelect($input: any, item: any) {
        $input.val(item.name);
    }

    onEnter($input: any, item: any) {
        console.log('+onEnter');
        if (item) {
            location.href = item.url;
        }
    }
}

export class AppHeader {
    _navbar: AppNavbar = null;
    _searchbar: AppSearchbar = null;

    constructor() {
        console.log("+AppHeader");
        this._navbar = new AppNavbar();
        this._searchbar = new AppSearchbar();
    }
};
