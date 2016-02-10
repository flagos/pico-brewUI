
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
      console.log(data)
      console.log(tank);

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


  Data = {
    labels : ["16:00","16:05","16:10","16:15","16:20","16:25"],
    datasets : [
      {
        label: "Hot tank",
        fillColor : "#b3e5fc",
  			strokeColor : "#01579b",
  			pointColor : "#fff",
  			pointStrokeColor : "#01579b",
        data : [50,45,42,44,48,50]
      },
      {
        label: "Malt tank",
        fillColor : "#ffecb3",
  			strokeColor : "#ff6f00",
  			pointColor : "#fff",
  			pointStrokeColor : "#ff6f00",
        data: [20, 25, 30, 30, 30, 30, 30]
      },
      {
        label: "Boil tank",
        fillColor : "#ffcdd2",
        strokeColor : "#b71c1c",
        pointColor : "#fff",
        pointStrokeColor : "#b71c1c",
        data: [0, 0, 7, 12, 20, 20, 20]
      }
    ]
  }
  chart_fill('volume-canvas', Data);

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
