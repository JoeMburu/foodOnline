let autocomplete;

window.initAutocomplete = function() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
                types: ['geocode', 'establishment'],
                //default in this app is "IN" - add your country code
                componentRestrictions: {'country': ['fi']},
        })
        // function to specify what should happen when the prediction is clicked
        autocomplete.addListener('place_changed', onPlaceChanged);
}

onPlaceChanged = function  (){
    console.log("Beginning of onPlaceChanged");
        var place = autocomplete.getPlace();

        // User did not select the prediction. Reset the input field or alert()
        if (!place.geometry){
                document.getElementById('id_address').placeholder = "Start typing...";
        }
        else{
                //console.log('place name=>', place)
        }
        // get the address components and assign them to the fields
        //console.log(place);
        var geocoder = new google.maps.Geocoder();
        var address = document.getElementById('id_address').value;
        geocoder.geocode({'address': address}, function(results, status) {
                if(status == google.maps.GeocoderStatus.OK) {
                    var latitude = results[0].geometry.location.lat();
                    var longitude = results[0].geometry.location.lng();
                    //console.log('lat=>', latitude);
                    //console.log('lng=>', longitude);

                    $('#id_latitude').val(latitude);
                    $('#id_longitude').val(longitude);
                    //$('#id_address').val(results[0].formatted_address);
                    $('#id_address').val(address);
                }
        });

        console.log("Place details=>", place);
        // loop through the address components and assign other address data
        for(var i=0; i<place.address_components.length; i++) {
            for(var j=0; j<place.address_components[i].types.length; j++) {
                // get country
                if (place.address_components[i].types[j] == 'country'){
                    //console.log('country=>', place.address_components[i].long_name);
                    $('#id_country').val(place.address_components[i].long_name);
                }
                // get state
                if (place.address_components[i].types[j] == 'administrative_area_level_1'){
                    //console.log('state=>', place.address_components[i].long_name);
                    $('#id_state').val(place.address_components[i].long_name);
                }
                // get city
                if (place.address_components[i].types[j] == 'locality'){
                    //console.log('city=>', place.address_components[i].long_name);
                    $('#id_city').val(place.address_components[i].long_name);
                }
                // get postal code
                if (place.address_components[i].types[j] == 'postal_code'){
                    //console.log('postal_code=>', place.address_components[i].long_name);
                    $('#id_post_code').val(place.address_components[i].long_name);
                    console.log("Post code: ", place.address_components[i].long_name)
                }

            }
        }				
}


