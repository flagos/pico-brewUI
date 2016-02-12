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

var callbackfortask = function(data) {
  var count = data["task"].length

  var html_data = ""

  for(var i=0; i<count; i++) {
    var task = data["task"][i];

    if (task["status"] == "done") {
      html_data += "<p> \
        <input type='checkbox' class='filled-in' id='check0' checked='checked' /> \
        <label for='check0' class='done'>"+ task["task name"]+"</label> \
      </p>"
    } else if (task["status"] == "waiting") {
      html_data += "<p> \
        <input type='checkbox' class='filled-in' id='check1' /> \
        <label for='check1' class='waiting'>"+ task["task name"]+"</label> \
      </p>"
    } else {
      html_data += "<p> \
        <input type='checkbox' id='check2' disabled='disabled' /> \
        <label for='check2' class='unavailable'>"+ task["task name"]+"</label> \
      </p> "
    }

  }

   $('#task-form').append(html_data)

}

$.getJSON( "/temperature/hot.json" , createCallbackforTank('hot'))
$.getJSON( "/temperature/mash.json", createCallbackforTank('mash'))
$.getJSON( "/temperature/boil.json", createCallbackforTank('boil'))
$.getJSON( "/volume.json", createCallbackforcard('volume'))
$.getJSON( "/power.json", createCallbackforcard('power'))

$.getJSON( "/task.json", callbackfortask)




  $(document).ready(function(){

    // initialiaze selectors
    $('select').material_select();

    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();

    // trigger for textarea
    $('#textarea1').trigger('autoresize');

  });
