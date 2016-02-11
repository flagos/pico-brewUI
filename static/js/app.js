// custon
if (!Array.prototype.last){
    Array.prototype.last = function(){
        return this[this.length - 1];
    };
};


  function chart_fill(canvas_id, chart_data) {

    var canvas = document.getElementById(canvas_id).getContext('2d');

    new Chart(canvas).Line(chart_data, {
      //Boolean - Whether to show horizontal lines (except X axis)
      scaleShowHorizontalLines: false,
      //Boolean - Whether to show vertical lines (except Y axis)
      scaleShowVerticalLines: false,
    });

  }

function createCallbackforTank(tank) {
    return function(data) {

      var Data = {
        labels : data["history"][0],
        datasets : [
          {
            fillColor : "#b3e5fc",
            strokeColor : "#01579b",
            pointColor : "#fff",
            pointStrokeColor : "#01579b",
            data : data["history"][1]
          }
        ]
      }
      chart_fill(tank+'-canvas', Data);

      $('#'+tank+'-temperature').html( data["value"] + " °C")

    }
  }

  $.getJSON( "/temperature/hot.json" , createCallbackforTank('hot'))
  $.getJSON( "/temperature/mash.json", createCallbackforTank('mash'))
  $.getJSON( "/temperature/boil.json", createCallbackforTank('boil'))

  var callbackforvolume = function(data) {

    Data = {
      labels : data["label"],
      datasets : [
        {
          label: "Hot tank",
          fillColor : "#b3e5fc",
    			strokeColor : "#01579b",
    			pointColor : "#fff",
    			pointStrokeColor : "#01579b",
          data: data["hot"]
        },
        {
          label: "Malt tank",
          fillColor : "#ffecb3",
    			strokeColor : "#ff6f00",
    			pointColor : "#fff",
    			pointStrokeColor : "#ff6f00",
          data: data["mash"]
        },
        {
          label: "Boil tank",
          fillColor : "#ffcdd2",
          strokeColor : "#b71c1c",
          pointColor : "#fff",
          pointStrokeColor : "#b71c1c",
          data: data["boil"]
        }
      ]
    }
    chart_fill('volume-canvas', Data);

    $('#hot-volume').html( 'hot: ' + data["hot"].last() + " L")
    $('#malt-volume').html( 'mash: ' + data["mash"].last() + " L")
    $('#boil-volume').html( 'boil: ' + data["boil"].last() + " L")
  }

  $.getJSON( "/volume.json", callbackforvolume)


  Data = {
    labels : ["16:00","16:05","16:10","16:15","16:20","16:25"],
    datasets : [
      {
        label: "Malt Power",
        //fillColor : "#ffecb3",
        fillColor : "transparent",
  			strokeColor : "#ff6f00",
  			pointColor : "#fff",
  			pointStrokeColor : "#ff6f00",
        data: [1100, 1200, 1300, 1640, 1480, 1400, 1520]
      },
      {
        label: "Hot Power",
        fillColor : "transparent",
  			strokeColor : "#01579b",
  			pointColor : "#fff",
  			pointStrokeColor : "#01579b",
        data : [600,520,550,480,450,500]
      },
      {
        label: "Boil Power",
        fillColor : "transparent",
        strokeColor : "#b71c1c",
        pointColor : "#fff",
        pointStrokeColor : "#b71c1c",
        data: [600, 400, 1000, 600, 500, 900, 800]
      }
    ]
  }
  chart_fill('power-canvas', Data);

  $(document).ready(function(){

    // initialiaze selectors
    $('select').material_select();

    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();

    // trigger for textarea
    $('#textarea1').trigger('autoresize');

  });
