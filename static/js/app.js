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

function createCallbackforTemperature(tank) {
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
        var task    = data["task"][i];
        var onclick = "onclick='callback_task_click(this, "+task["id"]+")' ";
        
        
        if (task["status"] == "done") {
            html_data += "<p > \
<input type='checkbox' class='filled-in' id='check0' checked='checked'  disabled='disabled'/> \
<label for='check0' class='done'>"+ task["task name"]+"</label> \
</p>"
        } else if (task["status"] == "waiting") {
            html_data += "<p > \
<input type='checkbox' class='filled-in' id='check1'  "+onclick+"/> \
<label for='check1' class='waiting'>"+ task["task name"]+"</label> \
</p>"
        } else {
            html_data += "<p > \
<input type='checkbox' id='check2' disabled='disabled' /> \
        <label for='check2' class='unavailable'>"+ task["task name"]+"</label> \
</p> "
        }
        
    }
    
    $('#task-form').html(html_data)
    
      
}

var callbackforrecipe = function(data) {
  var count = data["recipes"].length

  var html_data = ""
  html_data = "<tbody>"

  for(var i=0; i<count; i++) {
    var recipe = data["recipes"][i];

    html_data += "<tr class='recipe'> \
      <td class='td-delete'> <i class='material-icons delete-button'>delete</i></td> \
      <td class='recipe-name'>" + recipe["recipe_name"] + "</td> \
      <td class='recipe-step'>"+ recipe["step"] + "</td> \
      <td class='recipe-time'>"+recipe["time"]+"</td>"
      if (recipe["status"] != "pending")
        html_data += "<td> <i class='small material-icons'>pause</i></td>"
    html_data += "</tr> "

  }
  html_data += "</tbody>"

   $('#recipe-table').html(html_data)

}

var createCallbackforswitch = function(data) {
  var length = data["switchs"].length

  for (var i=0; i<length; i++){
    $('#switch-'+data["switchs"][i]["name"]).prop("checked", data["switchs"][i]["checked"])
}
}


function Callbackforswitch_click(switch_name) {
  $('#switch-' + switch_name).click(function(){
    var isChecked      = $('#switch-' + switch_name).prop("checked") ? 'True':'False';
    var display_status = $('#switch-' + switch_name).prop("checked") ? 'ON':'OFF';
      $.ajax({
        url : 'switch',
        type : 'GET',
        data : switch_name + '=' + isChecked,
        dataType : 'html',
        success : function(data, status){
          Materialize.toast(switch_name + ' set '+display_status , 4000)
          LoadElements();
        },
        error : function(data, status, error){
          Materialize.toast('Error occured while ' + switch_name + ' setting '+display_status , 20000)
          LoadElements();
        },
      });
  });

}

function lock(card, bool) {

  if (! bool ) {
    $('#card-'+card +' .lock').html('lock_open');
    $('#card-'+card+' :checkbox').removeAttr("disabled");
  } else {
    $('#card-'+card +' .lock').html('lock_outline');
    $('#card-'+card+' :checkbox').attr("disabled", true);
  }

}

function callbackforlock(data) {

  lock("valve", data["valve"]);
  lock("resistor", data["resistor"]);
  lock("pump", data["pump"]);

}

function callback_task_click(element, id) {
    //console.log(element, element.checked);
    $.ajax({
        url : '/update/task',
        type : 'GET',
        data: 'task_id='+id+'&task_status='+element.checked,
        dataType : 'html',
        success : function(data, status){
            console.log('ouf');
        },        
    });
}

function LoadElements()
{
  $.getJSON( "/temperature/hot.json" , createCallbackforTemperature('hot'))
  $.getJSON( "/temperature/mash.json", createCallbackforTemperature('mash'))
  $.getJSON( "/temperature/boil.json", createCallbackforTemperature('boil'))
  $.getJSON( "/volume.json", createCallbackforcard('volume'))
  $.getJSON( "/power.json", createCallbackforcard('power'))

  $.getJSON( "/task.json", callbackfortask)
  $.getJSON( "/recipe.json", callbackforrecipe)

  $.getJSON( "/valve.json", createCallbackforswitch)
  $.getJSON( "/resistor.json", createCallbackforswitch)
  $.getJSON( "/pump.json", createCallbackforswitch)

  $.getJSON("/lock.json", callbackforlock)
}

  function createCallbackforlock(card) {
    return function () {

      $.ajax(
        {
          url : 'lock',
          type : 'GET',
          data : card,
          dataType : 'html',
          success : function(data, status){
            LoadElements();
          },
          error : function(data, status, error){
            Materialize.toast('Error occured while setting ' + lock, 20000)
            LoadElements();
          },
        }

      );

    };
  };


var callback_submit_url = function() {

var url      = $('#input-url').val();
 $.ajax(
    {
      url : 'add/recipe',
      type : 'GET',
      data : "url="+url,
      dataType : 'html',
      success : function(data, status){
        Materialize.toast('Recipe added',  4000)
        LoadElements();
      },
      error : function(data, status, error){
        Materialize.toast('Error occured while adding recipe ', 20000)
        LoadElements();
      },
    })


  }

  $(document).ready(function(){

      // initialiaze selectors
      $('select').material_select();
      
      // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
      $('.modal-trigger').leanModal();
      
      // trigger for textarea
      $('#textarea1').trigger('autoresize');
      
      LoadElements();
      Chart.defaults.global["animation"] = false;
      setInterval( LoadElements, 1000 );
      
      Callbackforswitch_click('resistor-hot');
      Callbackforswitch_click('resistor-mash');
      Callbackforswitch_click('resistor-boil');
      
      Callbackforswitch_click('valve-hot');
      Callbackforswitch_click('valve-mash');
      Callbackforswitch_click('valve-boil');
      
      Callbackforswitch_click('pump');
      
      
      $('#valve-lock').on('click', createCallbackforlock('valve'));
      $('#card-resistor .lock').on('click',createCallbackforlock('resistor'));
      $('#card-pump .lock').on('click',createCallbackforlock('pump'));
      
      $('#submit-url').on('click',callback_submit_url);
      
      //$('#card-task').change(callback_task_click);


      

      console.log('finish loading');
     
  });
