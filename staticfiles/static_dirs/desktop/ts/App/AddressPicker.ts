import { AppEvent, GoogleMap, FormUtil, AppGeo, UIToast, UIOverlay } from "..";
import { AppUtil } from "./AppLib";


export class AddressPicker {

    _$html = $(`<div id="locus_addr_picker" data-type="persist" style="margin:0px auto; width:80%; padding:2px;">
                    <div class="ui-block" >
                        <div class="ui-block-head">
                            <div style="text-align: center;">
                                <h3>ADDRESS</h3>
                            </div>
                            <div>
                            </div>
                        </div>
                        <div class="ui-block-body">
                            <div style="border: 1px solid #ddd;" class="wt-overlay-scroll" >
                                <div style="display:table-cell; width: 50%;">
                                    <table class="ui-info-table">
                                        <tr><td>LOCATION</td></tr>
                                        <tr><td>
                                            <input type="text" name="gmap_search_input" id="gmap_search_input" class="ui-input" style="max-width:50em; padding-right:7em;" />
                                            <a class="ui-btn-a" style="width:7em; margin-left: -7em;" onclick="locateMe()"> Locate Me </a>
                                        </td></tr>
                                        <tr><td>
                                        <div id="gmap_box" style="width: 95%; height: 300px; border: 2px solid #bbb;" >
                                            <h1>&nbsp;</h1>
                                        </div>
                                        </td></tr>
                                        <tr><td>
                                            <h2 style="font-size: 1em; font-weight:bold;">
                                                Choose your business location from map to increase Visibility of your business on Internet
                                            </h2>
                                        </td></tr>
                                    </table>
                                </div>

                                <div style="display:table-cell; width: 50%;" >
                                    <form action="/locus/address/create/" method="POST" class="ajax-form locus_addr_form" >
                                    ${AppUtil.csrfField()}
                                    <input type="hidden" name="A_id" value="-1" />
                                    <input type="hidden" name="A_location" value="12.964914,77.596683" />
                                    <table class="ui-info-table">
                                        <tr><td>NAME</td></tr>
                                        <tr><td>
                                            <input type="text" name="A_name" class="ui-input" placeholder="House / Office Building Number" />
                                        </td></tr>
                                        <tr><td>PINCODE / ZIPCODE</td></tr>
                                        <tr><td><input type="text" name="A_pincode" class="ui-input" placeholder="176039"/> </td></tr>
                                        <tr><td>ADDRESS</td></tr>
                                        <tr><td><textarea name="A_address" class="ui-input" placeholder="Full Address" > </textarea> </td></tr>
                                        <tr><td>PERSON / INCHARGE</td></tr>
                                        <tr><td><input type="text" name="A_pname" class="ui-input" placeholder="Ramesh Kumar" /> </td></tr>
                                        <tr><td>PHONE</td></tr>
                                        <tr><td><input type="text" name="A_phone" class="ui-input" placeholder="+91 9876543210" /> </td></tr>
                                        <tr><td><input type="submit" value="Save" class="ui-btn" /></td></tr>
                                    </table>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`);
    _$form: any = null;

    BeforeSaveEvent = new AppEvent();
    AfterSaveEvent = new AppEvent();
    CloseEvent = new AppEvent();
    _googleMap = new GoogleMap();

    constructor(options: any) {
        this._$form = this._$html.find('.locus_addr_form');
        this._$form.data('data-handler', this);
        this.loadMap(()=>{});
    }

    show(vals?: any) {
        if (vals !== undefined) {
            this.updateVals(vals);
        }
        let config = {onClose: ()=>{ this.close() }};
        UIOverlay.Instance().show(this._$html, config);
    }

    hide() {
        this.close();
    }

    close() {
        this.CloseEvent.trigger({}, null);
        this._$html.detach();
        // reset id before closing.
        FormUtil.setValByName(this._$form, 'A_id', -1);
        UIOverlay.Instance().hide();
    }

    updateVals(vals?: any) {
        FormUtil.fillByName(this._$form, vals);
    }

    before(e: any) {
        console.log('+BeforeAdrReq');
        return this.BeforeSaveEvent.trigger(e, null);
    }

    after(e: any) {
        console.log('+AfterAdrRes');
        return this.AfterSaveEvent.trigger(e, null);
    }

	loadMap(OnLoad: any) {
        let This = this;
		This._googleMap.load(function(e: any) {
			if (e.status) {
				This.initMap();
				OnLoad(e);
			}
		});
	}

	initMap() {
		let mapBox = this._$html.find("#gmap_box").get(0);
		let mapInput = this._$html.find("#gmap_search_input").get(0);
		this._googleMap.attach(mapBox);
		this._googleMap.initPlaceSearch(mapInput);
		this._googleMap.AddressFoundEvent.sub(this.OnFound.bind(this));
	}

	OnFound(e: any, data: any) {
		console.log("+OnAddressFound");
		if (!data.status)
			return;

		let faddr = data.address.formatted_address;
		let loc = data.address.geometry.location;
		loc = loc.lat() + ',' + loc.lng();
		console.log('loc : '+loc);
		let parts = faddr.split(",");
		let len = parts.length;
		let name = parts[0];
		let stateStr = parts[len - 2];
		let index = stateStr.lastIndexOf(" ");
		let state = stateStr.substr(0, index);
		let pincode = stateStr.substr(index + 1);
		let country = parts[len - 1];
		let vals = {
			'A_name': name,
			'A_address': faddr,
			'A_pincode': pincode,
			'A_location': loc,
		};
		FormUtil.fillByName(this._$form, vals);
	}

	locateMe()
	{
		this.loadMap(function(e: any) {
			if (e.status) {
					AppGeo.locate(function(lt: number, lg: number) {
					this._googleMap.updateLoc(lt,lg);
				});
			} else  {
				UIToast.show("Failed to load maps");
			}
		});
    }
}