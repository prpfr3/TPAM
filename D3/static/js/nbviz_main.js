/* global $, _, crossfilter, d3  */

(function(nbviz) {
    'use strict';

    // The main JS entry point

    var query_winners = 'winners?projection=' +
        JSON.stringify( {"mini_bio":0, "bio_image":0} );
    
    // Load the initial data required by the Nobel-viz
    // The queue function gets the data in parallel....
    var q = queue()
        // json country data available at https://github.com/topojson/world-atlas
        .defer(d3.json, "../../static/data/world-110m.json")
        //.defer(d3.json, "../../static/data/uk.json")//
        .defer(d3.csv, "../../static/data/world-country-names-nobel.csv")
        .defer(d3.json, "../../static/data/winning_country_data.json");
    
    // The $STATIC_API flag dictates whether we are using static
    // files or using the MongoDB based EVE-API
    if(window.$STATIC_API){
        q.defer(nbviz.getDataFromAPI, '_winners');
    }
    else{
        q.defer(nbviz.getDataFromAPI, query_winners);
    }
    
    // The await callback function awaits the results and then calls the ready function
    q.await(ready);

    function ready(error, worldMap, countryNames, countryData, winnersData) {
        // LOG ANY ERROR TO CONSOLE 
        if(error){
            return console.warn(error);
        }
        // STORE OUR COUNTRY-DATA DATASET
        nbviz.data.countryData = countryData;
        // MAKE OUR FILTER AND ITS DIMENSIONS
        nbviz.makeFilterAndDimensions(winnersData);
        // INITIALIZE MENU AND MAP
        nbviz.initMenu();
        nbviz.initMap(worldMap, countryNames);
        // TRIGGER UPDATE WITH FULL WINNERS' DATASET
        nbviz.onDataChange();
    }
}(window.nbviz = window.nbviz || {}));
