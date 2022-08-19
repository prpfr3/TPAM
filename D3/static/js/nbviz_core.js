/* global $, _, crossfilter, d3  */
(function(nbviz) {
    'use strict';
    
    // The shared JS utilities and constants
    // The nbviz namespace is used to denote anything shared across modules
    nbviz.ALL_CATS = 'All Categories';
    nbviz.TRANS_DURATION = 2000; //length in milliseconds
    nbviz.MAX_CENTROID_RADIUS = 30;
    nbviz.MIN_CENTROID_RADIUS = 2;
    nbviz.COLORS = {palegold:'#E6BE8A'}; //any named colours used
    
    nbviz.data = {};  // the main data object
    nbviz.valuePerCapita = 0;
    nbviz.activeCountry = null;
    nbviz.activeCategory = nbviz.ALL_CATS;
    
    nbviz.CATEGORIES = [
        "Chemistry", "Economics", "Literature", "Peace", "Physics", "Physiology or Medicine"
    ];
    
    
    nbviz.categoryFill = function(category){
        var i = nbviz.CATEGORIES.indexOf(category);
        return d3.hcl(i / nbviz.CATEGORIES.length * 360, 60, 70);
    };

        
    // $EVE_API (by default 'http://localhost:5000/api/') is set in
    // index_static.html to use STATIC FILES and in index-mongo.html to use MONGODB;
    
    // A wrapper function to get data from the RESTful API using a resource string and some query data
    nbviz.getDataFromAPI = function(resource, callback){
        d3.json($EVE_API + resource, function(error, data) {
            
            if(error){
                return callback(error);
            }
            // callback has an error item (null here) and the data
            if('_items' in data){
                callback(null, data._items); // Mongodb items case
            }
            else{
                callback(null, data); // Individual Resource case
            }
            
        });
    };
    
    var nestDataByYear = function(entries) {
        return nbviz.data.years = d3.nest()
            .key(function(w) {
                return w.year;
            })
            .entries(entries);
    };

    nbviz.makeFilterAndDimensions = function(winnersData){
        // ADD OUR FILTER AND CREATE CATEGORY DIMENSIONS using the CROSSFILTER function
        nbviz.filter = crossfilter(winnersData);
        nbviz.countryDim = nbviz.filter.dimension(function(o){
            return o.country;
        });

        nbviz.categoryDim = nbviz.filter.dimension(function(o) {
            return o.category;
        });

        nbviz.genderDim = nbviz.filter.dimension(function(o) {
            return o.gender;
        });
    };
    
    nbviz.filterByCountries = function(countryNames) {
        
        if(!countryNames.length){
            nbviz.countryDim.filter();
        }
        else{
            nbviz.countryDim.filter(function(name) {
                return countryNames.indexOf(name) > -1;
            });
        }
        
        if(countryNames.length === 1){
            nbviz.activeCountry = countryNames[0];
        }
        else{
            nbviz.activeCountry = null;
        }
    };

    nbviz.filterByCategory = function(cat) {
        nbviz.activeCategory = cat;
        
        if(cat === nbviz.ALL_CATS){
            nbviz.categoryDim.filter();
        }
        else{
            nbviz.categoryDim.filter(cat);
        }
    };

    nbviz.getCountryData = function() {
        // using a Crossfilter dimension of countryDim to group key/value pairs
        var countryGroups = nbviz.countryDim.group().all();

        // make main data-ball
        var data = countryGroups.map( function(c) {
            var cData = nbviz.data.countryData[c.key];
            var value = c.value;
            // if per-capita value then divide by pop. size
            if(nbviz.valuePerCapita){
                value /= cData.population;
            }
            return {
                key: c.key,
                value: value,
                code: cData.alpha3Code,
                // population: cData.population
            };
        })
            .sort(function(a, b) {
                return b.value - a.value; // descending
            });

        return data;
    };

    // The main function for spotting and acting on any changes to the selection data
    // Called from nbviz_main.js to initialize and then from nbviz_menu whenever the user changes the data
    nbviz.onDataChange = function() {
        // returns the main dataset of winners by country and some country data such as population and code
        var data = nbviz.getCountryData();
        nbviz.updateBarChart(data);
        nbviz.updateMap(data);
        // updateList passes an array of selected winners to the updateList Method
        // top returns a specified number of objects, here Infinity which means all
        nbviz.updateList(nbviz.countryDim.top(Infinity));
        // creates nested data for our timechart
        data = nestDataByYear(nbviz.countryDim.top(Infinity));
        nbviz.updateTimeChart(data);
    };
    
}(window.nbviz = window.nbviz || {}));
