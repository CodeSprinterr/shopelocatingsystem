function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

function searchbyitemcall(){
    if(document.getElementById("itemsearch").value == ""){
        alert("please enter data to search");
    }
    else{
        window.location.href ="searchbyitem?itname="+document.getElementById("itemsearch").value+"&state="+getCookie("state")+"&district="+getCookie("district")+"&city="+getCookie("city");
    }
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////directfunctionload/////////////////

$(function () {

    $("#change").click(function () {
        document.getElementById("city").disabled = false;
        document.getElementById("city").value = "";
    })
    document.getElementById("city").value = getCookie("city");

    $("#city").autocomplete({
        source: '/getlocation',
        minLength: 0,
        scroll: true,
//in development
        select: function (event, ui) {
            var expiryDate = new Date();
            expiryDate.setMonth(expiryDate.getMonth() + 12);
            document.cookie = "state="+ui.item.state+"; expires=" + expiryDate.toGMTString();
            document.cookie = "district="+ui.item.dist+"; expires=" + expiryDate.toGMTString();
            document.cookie = "city="+ui.item.label+"; expires=" + expiryDate.toGMTString();
            window.location.reload();
           
        }
        
    }).focus(function () {
        $(this).autocomplete("search", "");
    }).autocomplete("instance")._renderItem = function (ul, item) {
        return $("<li>")
            .append("<div style='font-size: 12px;'>" +"city : "+ item.label + "<br>" +"District : "+ item.dist +  "<br>" +"State : "+ item.state + "</div>")
            .appendTo(ul);
    };
    $("#itemsearch").autocomplete({
        source: function (request, response) {
            jQuery.get("itemlist", {
                term: request.term,
                st:  getCookie("state"),
                dt:  getCookie("district"),
                ct : getCookie("city")
            }, function (data) {
                
                response(data);
            });
        },
        minLength: 0,
        scroll: true,

        select: function (event, ui) {
           
            window.location.href =  "searchbyitem?itname="+ui.item.label+"&state="+getCookie("state")+"&district="+getCookie("district")+"&city="+getCookie("city");
        }

    }).focus(function () {
        $(this).autocomplete("search", "");
    });


});
