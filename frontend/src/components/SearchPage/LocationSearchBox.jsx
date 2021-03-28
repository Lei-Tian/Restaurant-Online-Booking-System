import React from 'react';
import { GooglePlaceAutoComplete } from '../../_components';
import { useSearchLocation } from './global.state';

function LocationSearchBox() {
    const [location, setSearchLocation] = useSearchLocation();
    return (
        <div>
            <GooglePlaceAutoComplete
                location={location}
                setLocation={setSearchLocation}
            />
        </div>
    );
}

export { LocationSearchBox };
