$(function () {

    

    $("#state").autocomplete({
        source: '/state',
        minLength: 0,
        scroll: true,

        select: function (event, ui) {
            document.getElementById("district").value = ""
            document.getElementById("city1").value = ""
            document.getElementById("area").value = "";
            statefunc(ui.item.value)
        }

    }).focus(function () {
        $(this).autocomplete("search", "");
    });
});

function statefunc(tempdata) {
    document.getElementById("district").disabled = false;
    document.getElementById("city1").disabled = true;
    document.getElementById("area").disabled = true;
    document.getElementById("search").disabled = true;


    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {

            var districtdata = this.responseText;

            var a = eval(districtdata);
            $("#district").autocomplete({
                source: function (request, response) {
                    var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
                    response($.map(a, function (item) {
                        if (matcher.test(item)) {
                            return (item)
                        }
                    }));
                },
                delay: 0,
                minLength: 0,
                scroll: true,
                select: function (event, ui) {
                    document.getElementById("city1").value = ""
                    document.getElementById("area").value = "";
                    districtfunc(ui.item.value)
                }

            }).focus(function () {
                $(this).autocomplete("search", "");
            });


        }
    };

    xhttp.open("post", "district", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("statename=" + tempdata);

}





function districtfunc(tempdata) {
    document.getElementById("city1").disabled = false;
    document.getElementById("area").disabled = true;
    document.getElementById("search").disabled = true;



    $("#city1").autocomplete({
        source: function (request, response) {
            jQuery.get("citylist", {
                term: request.term,
                statedata:  document.getElementById("state").value,
                districtdata:  document.getElementById("district").value,
            }, function (data) {
                // assuming data is a JavaScript array such as
                // ["one@abc.de", "onf@abc.de","ong@abc.de"]
                // and not a string
                response(data);
            });
        },
        delay: 0,
        minLength: 0,
        scroll: true,
        select: function (event, ui) {
            document.getElementById("area").value = "";
            cityfunc(ui.item.value);
        }

    }).focus(function () {
        $(this).autocomplete("search", "");
    });

}

function cityfunc(tempdata) {

    document.getElementById("area").disabled = false;
    document.getElementById("search").disabled = true;

    $("#area").autocomplete({
        source: function (request, response) {
            jQuery.get("arealist", {
                term: request.term,
                statedata:  document.getElementById("state").value,
                districtdata:  document.getElementById("district").value,
                citydata : document.getElementById("city1").value,
            }, function (data) {
                
                response(data);
            });
        },
        delay: 0,
        minLength: 0,
        scroll: true,
        select: function (event, ui) {
            document.getElementById("search").disabled = false;
            
        }
        

    }).focus(function () {
        $(this).autocomplete("search", "");
    });


}
/*
function searchdata(){
    var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        
    }
  };
  xhttp.open("GET", "searchbyarea?statename="+document.getElementById("state").value
  +"&districtname="+document.getElementById("district").value+
   "&cityname="+document.getElementById("city").value+
   "&areaname="+document.getElementById("area").value,true);
  xhttp.send();
}*/