<script type='text/javascript>
function loadMapScenario() {
            map = new Microsoft.Maps.Map(document.getElementById('myMap'), {});
            Microsoft.Maps.Events.addHandler(map, 'dblclick', function (e) { addPin(e); });
        }
var map = null;
        var noPins = true;
        var mode = 1;
        var directionsManager;
        var searchManager;
        var sourcepoints = "[";
        var sourcepointsnames = "[";
        var sourcepointsnamescount = 0;
        var destinationpoints = "[";
        var noofdestinationpoints = 0;
        var colors = ['#ff0000', '#20b2aa', '#320f3c', '#cd9b1d', '#ffd700', '#eb5e88', '#008000', '#c0c0c0']



        function GetDynamicTextBox(value) {
            return '<input name = "DynamicTextBox" type="text" style="width:100%" value = "' + value + '" />'
        }

        function GetDynamicTextBoxSrc(value) {
            return '<input name = "DynamicTextBoxSrc" type="text" style="width:100%" value = "' + value + '" />'
        }




        function defPoint(val) {

            var div = document.createElement('DIV');
            //var res1 = val.split(",");
            //var loc = new Microsoft.Maps.Location(Number(res1[0]), Number(res1[1]));

            div.innerHTML = GetDynamicTextBox(val);
            document.getElementById("Listdst").appendChild(div);
        }



        function addPin(e) {


            if (e.targetType == "map") {
                var point = new Microsoft.Maps.Point(e.getX(), e.getY());
                var loc = e.target.tryPixelToLocation(point);
                var pin = new Microsoft.Maps.Pushpin(loc);

                var div = document.createElement('DIV');

                if (mode == 1) {
                    div.innerHTML = GetDynamicTextBox(loc.latitude + "," + loc.longitude);
                    document.getElementById("Listdst").appendChild(div);
                    destinationpoints = destinationpoints + "[" + loc.latitude + "," + loc.longitude + "],";
                    noofdestinationpoints = noofdestinationpoints + 1;

                }
                else {
                    div.innerHTML = GetDynamicTextBoxSrc(loc.latitude + "," + loc.longitude);
                    document.getElementById("ListSrc").appendChild(div);
                    sourcepoints = sourcepoints + "[" + loc.latitude + "," + loc.longitude + "],";
                    sourcepointsnamescount = sourcepointsnamescount + 1;
                    sourcepointsnames = sourcepointsnames + "'S" + sourcepointsnamescount + "',";


                }

                map.entities.push(pin);

            }
        }
        function crap() {
            mode = 1;
            document.getElementById("inst").value = "Double click on Map to Choose Destination Points. Click on Find Route when done with Source and Destination Points!";
            return false;
        }
        function crap2() {
            mode = 0;
            document.getElementById("inst").value = "Double click on Map to Choose Source Points. Click on Find Route when done with Source and Destination Points!";
            return false;
        }


        function processRequest(e) {

            alert(xhr.responseText);


        }
        function setText(str) {

            document.getElementById("TextBox2").value = str;
            var point = new Microsoft.Maps.Location(12.98, 74.4);

            var pin = new Microsoft.Maps.Pushpin(point);

            map.entities.push(pin);
        }

        function drawRoute(str1, str2, colind, pintype, i) {

            var res1 = str1.split(",");
            var res2 = str2.split(",");
            var col = colors[Number(colind)];

            var pintyp = Number(pintype);
            var point1 = new Microsoft.Maps.Location(Number(res1[0]), Number(res1[1]));
            var point2 = new Microsoft.Maps.Location(Number(res2[0]), Number(res2[1]));

            //alert(res1[0]+res1[1]+" "+res2[0]+res2[1]);
            if (pintyp == 0) {
                var ind = Number(i) - 1;
                var pin = new Microsoft.Maps.Pushpin(point1, {
                    text: "" + ind
                });
            }

            else
                var pin = new Microsoft.Maps.Pushpin(point1, {
                    text: "S"
                });

            map.entities.push(pin);

            var coords = [point1, point2];
            var line = new Microsoft.Maps.Polyline(coords, { strokeColor: Microsoft.Maps.Color.fromHex(col) });

            //Add the polyline to map
            map.entities.push(line);

        }

        function optCall() {
            if ((document.getElementById("Listdst").childElementCount == 1) || (document.getElementById("ListSrc").childElementCount == 1)) {
                alert("Double Click on Map to select the Destination and Source Points");
            }
            else {

                var inputToRouteService = new Object();
                inputToRouteService.Choice = "1";
                inputToRouteService.numberOfDesinations = noofdestinationpoints.toString();
                inputToRouteService.preference = "0";
                inputToRouteService.nclus = "-1";
                inputToRouteService.DesinationRoutes = destinationpoints.replace(/,$/, "]");
                inputToRouteService.SourceRoutes = sourcepoints.replace(/,$/, "]");;
                inputToRouteService.sourcepointsnames = sourcepointsnames.replace(/,$/, "]");;
                var inputToRouteServiceJSON = JSON.stringify(inputToRouteService);

                //  { "Choice":"1", "numberOfDesinations":"4", "preference":"0", "nclus":"-1", "DesinationRoutes":"[[13.097930226887641,77.38407135009767],[13.005286559379101,77.38595962524415],[12.989145623674318,77.44947433471681],[13.093248709483944,77.53251552581788]]", "SourceRoutes":"[[13.055876981865168,77.43415355682374],[13.073393071348988,77.47462272644044]]", "sourcepointsnames":"['S1','S2']" }
                //  { "Choice":"1", "numberOfDesinations":"4", "preference":"0", "nclus":"-1", "DesinationRoutes":"[[13.126686165886681,77.46543884277345],[13.08104290655325,77.38939285278322],[13.043418482235807,77.44947433471681],[13.131367046940397,77.61169433593751]]", "SourceRoutes":"[[13.148919556130394,77.40261077880861],[13.113813283244695,77.56774902343751]]", "sourcepointsnames":"[S1,S2]" }

                var url = "http://localhost:8185/RouteOptimizer";
                var client = new XMLHttpRequest();
                client.open("PUT", url, false);
                client.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                client.setRequestHeader("Connection", "close");

                client.send("data=" + encodeURIComponent(inputToRouteServiceJSON));
                if (client.status == 200)
                    alert("The request succeeded!\n\nThe response representation was:\n\n" + client.responseText)
                else
                    alert("The request did not succeed!\n\nThe response status was: " + client.status + " " + client.statusText + ".");






                drawRoute('13.055876981865168,77.43415355682374', '12.989145623674318,77.44947433471681', '0', '1', '1');
                drawRoute('12.989145623674318,77.44947433471681', '13.005286559379101,77.38595962524415', '0', '0', '2');
                drawRoute('13.005286559379101,77.38595962524415', '13.097930226887641,77.38407135009767', '0', '0', '3');
                drawRoute('13.097930226887641,77.38407135009767', '13.055876981865168,77.43415355682374', '0', '0', '4');
                drawRoute('13.073393071348988,77.47462272644044', '13.093248709483944,77.53251552581788', '1', '1', '1');
                drawRoute('13.093248709483944,77.53251552581788', '13.073393071348988,77.47462272644044', '1', '0', '2');

            }
        }
</script>