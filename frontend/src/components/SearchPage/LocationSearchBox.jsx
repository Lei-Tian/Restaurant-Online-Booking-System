import React from 'react';
import { GooglePlaceAutoComplete } from '../../_components';
import { useSearchLocation } from './global.state';

function LocationSearchBox() {
    const [_, setSearchLocation] = useSearchLocation();
    return (
        <div>
            <GooglePlaceAutoComplete setLocation={setSearchLocation} />
        </div>
    );
}

export { LocationSearchBox };
