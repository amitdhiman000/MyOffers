import {AppEventHandler, AppGeo} from './AppUtils';
import {UIToast} from './UIToast';

const url = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCMz94217XzpYaxnQRagzgCwpy4dfBM1Ho&libraries=places&callback=__onGoogleMapLoaded';

export class GoogleMapsLoader {
    private static promise: any;

    public static load() {
        // First time 'load' is called?
        if (!GoogleMapsLoader.promise) {

            // Make promise to load
            GoogleMapsLoader.promise = new Promise( resolve => {
                // Set callback for when google maps is loaded.
                window['__onGoogleMapLoaded'] = (ev: any ) => {
                    resolve('google maps api loaded');
                };

                let node = document.createElement('script');
                node.src = url;
                node.type = 'text/javascript';
                document.getElementsByTagName('head')[0].appendChild(node);
            });
        }

        // Always return promise. When 'load' is called many times, the promise is already resolved.
        return GoogleMapsLoader.promise;
    }
}


declare var google: any;

export class GoogleMap {
	_IsInit = false;
	_Map = null;
	_Marker = null;
	_Geocoder = null;
	_Timeout = null;
	_LatLong = {lat:12.964914, lng:77.596683};
    AddressFoundEvent: AppEventHandler = new AppEventHandler();
    
    constructor(mapBox: any, config: any) {
        GoogleMapsLoader.load();
    }

    attach(mapBox: any) {
		console.log("+GoogleMap::init");
		let This = this;
		let myLatlng = new google.maps.LatLng(This._LatLong.lat, This._LatLong.lng);
		let mapOpts = {
			zoom: 18,
			center: myLatlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		}

		This._Map = new google.maps.Map(mapBox, mapOpts);
		This._Marker = new google.maps.Marker({
			position: myLatlng,
			map: This._Map,
			draggable: true,
			title: "Your Location"
		});
		This._Geocoder = new google.maps.Geocoder();

		google.maps.event.addListener(This._Marker, 'dragend', function (e) {
			This.updateLoc(e.latLng.lat(), e.latLng.lng());
		});

		google.maps.event.addListener(This._Map, 'drag', function (e) {
			let center = this.getCenter();
			clearTimeout(This._Timeout);
			This._Timeout = setTimeout(function() {
				This._Marker.setPosition(center);
				This.updateLoc(center.lat(), center.lng());
			}, 50);
		});

		This._IsInit = true;
		AppGeo.Instance().locate(function(lt: number, lg: number) {
			This.updateLoc(lt,lg);
		});
    }
    
	initPlaceSearch(input: any) {
		console.log('+GoogleMap::initPlaceSearch');
		let This = this;
		let autocomplete = new google.maps.places.Autocomplete(input);

		autocomplete.addListener('place_changed', function() {
			This._Marker.setVisible(false);
			let place = autocomplete.getPlace();
			if (!place.geometry) {
				UIToast.Instance().show("No details available for : '" + place.name + "'");
				return;
			}

			console.log(place);
			// If the place has a geometry, then present it on a map.
			if (place.geometry.viewport) {
				This._Map.fitBounds(place.geometry.viewport);
			} else {
				This._Map.setCenter(place.geometry.location);
				This._Map.setZoom(17);
			}
			This._Marker.setPosition(place.geometry.location);
			This._Marker.setVisible(true);
			This.AddressFoundEvent.trigger({status:true, address:place});
		});
    }
    
	update() {
		if (this._Map) {
			google.maps.event.trigger(this._Map, 'resize');
			if (this._Marker) {
				this._Map.setCenter(this._Marker.getPosition());
			}
		}
    }
    
	updateLoc(lat: number, lng: number) {
		console.log('[' +lat + ' ### ' + lng+ ']');
		if (lat != 0 && lng != 0) {
			let This = this;
			let pos = new google.maps.LatLng(lat, lng);
			This._Marker.setPosition(pos);
			This._Map.panTo(pos);
			return This.getAddress(pos, function(data){
				This.AddressFoundEvent.trigger(data);
			});
		}
    }
    
	getAddress(loc: any, OnFound: any) {
		if (!this._IsInit)
			return;
		this._Geocoder.geocode({
			'location': loc
			},
			function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					console.log(results[0]);
					OnFound({status:true, 'address':results[0]});
				} else {
					console.log('Geocode failed reason: ' + status);
					OnFound({status:false, address:''});
				}
			}
		);
	}
}