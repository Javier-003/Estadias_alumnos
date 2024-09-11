
// selecciona el mes de la fecha, ejemplo "2021-03" = "03" y devuelve en entero 3

function SelecMes(fecha){
    var Cadfecha;
    Cadfecha=fecha.split("-");
    return parseInt(Cadfecha[1]);
}   
//  Seleciona el año de la fecha, ejemplo "2021-03" =  "2021"y lo regresa

function Anio(fecha){
    var Cadfecha;
    Cadfecha=fecha.split("-");
    return Cadfecha[0];
}

// une los meses de las fechas "10 Enero 2021" y "15 Abril 2021" = "Enero-Abril 2021" y regresa el periodo
function UnirFechas(fecha1,fecha2){
    var pt1,pt2,periodo; 
    
    pt1=fecha1.split(" ");
    pt2=fecha2.split(" ");
    periodo=pt1[1]+"-"+pt2[1]+" "+pt2[2];
    // document.write(periodo);
    return periodo;
}
// {} []  Convierte el numero de mes en palabra, ejemplo 5 = "Mayo" y lo regresa  
function MesNum_MesPalabra(mes){
var Mess;
switch (mes) {
    case 1: Mess = "enero"; return Mess; break;
    case 2: Mess = "febrero"; return Mess; break;
    case 3: Mess = "marzo"; return Mess; break;
    case 4: Mess = "abril"; return Mess; break;
    case 5: Mess = "mayo"; return Mess; break;
    case 6: Mess = "junio"; return Mess; break;
    case 7: Mess = "julio"; return Mess; break;
    case 8: Mess = "agosto"; return Mess; break;
    case 9: Mess = "septiembre"; return Mess; break;
    case 10: Mess = "octubre"; return Mess; break;
    case 11: Mess = "noviembre"; return Mess; break;
    case 12: Mess = "diciembre"; return Mess; break;
}
}