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

  function createCallbackforcard(card) {

  return function(data) {

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
    chart_fill(card+'-canvas', Data);

    $('#hot-'+card).html( 'hot: ' + data["hot"].last() + (card=='volume'?" L":" W"))
    $('#malt-'+card).html( 'mash: ' + data["mash"].last() + (card=='volume'?" L":" W"))
    $('#boil-'+card).html( 'boil: ' + data["boil"].last() + (card=='volume'?" L":" W"))
  }
}

$.getJSON( "/temperature/hot.json" , createCallbackforTank('hot'))
$.getJSON( "/temperature/mash.json", createCallbackforTank('mash'))
$.getJSON( "/temperature/boil.json", createCallbackforTank('boil'))
$.getJSON( "/volume.json", createCallbackforcard('volume'))
$.getJSON( "/power.json", createCallbackforcard('power'))





  $(document).ready(function(){

    // initialiaze selectors
    $('select').material_select();

    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();

    // trigger for textarea
    $('#textarea1').trigger('autoresize');

  });
