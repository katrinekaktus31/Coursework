    require([
      "esri/Map",
      "esri/views/MapView",
      "esri/layers/FeatureLayer",
      "esri/layers/GeoJSONLayer"
    ], function(
      Map, MapView, FeatureLayer, GeoJSONLayer
    ) {

      const map = new Map({
          basemap: "gray-vector",
        });

      const view = new MapView({
            container: "viewDiv",
            center: [36, 50],
            zoom: 4,
            map: map
        });

      const template = {
          title: "Earthquake Info",
          content: "Magnitude {mag} hit {place} on {datetime}",
          fieldInfos: [
            {
              fieldName: "datetime",
              format: {
                dateFormat: "short-date-short-time"
              }
            }
          ]
        };

      const renderer = {
          type: "simple",
          field: "mag",
          symbol: {
            type: "simple-marker",
            color: "orange",
            outline: {
              color: "white"
            }
          },
          visualVariables: [{
            type: "size",
            field: "mag",
            stops: [{
                value: 2.5,
                size: "4px"
              },
              {
                value: 8,
                size: "40px"
              }
            ]
          }]
        };


      // var geoJsonLayer4 = new GeoJSONLayer({
      // url: "D:/python_project/PC_project/diploma/q_file.json",
      // renderer: renderer
      // });
      geojsonUrl = "../tableQuake.geojson"
      // let getjsonUrl = location.pathname.replace(/\/[^/]+$/, "");
      // geojsonUrl = geojsonUrl +"/q_file.json";
      // geojsonUrl = location.href + geojsonUrl
      //you might need this line like => geojsonUrl = location.href + geojsonUrl;
      //try the log and change code accordingly
      // console.log("geo json absolute url:"+geojsonUrl);
      const geoJSONLayer = new GeoJSONLayer({
          url: geojsonUrl,
          renderer: renderer,
          popupTemplate: template,
      });

      map.add(geoJSONLayer);

    });
