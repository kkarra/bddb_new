// Using aoColumnDefs
//$(document).ready( function() {
//  $('#example').dataTable( {
//    "aoColumnDefs": [
//      { "sType": "html", "aTargets": [ 0 ] }
//    ]
//  } );
//} );
 
 
// Using aoColumns
//$(document).ready( function() {
//  $('#example').dataTable( {
//    "aoColumns": [
//      { "sType": "html" },
//      null,
//      null,
//      null,
//      null
//    ]
//  } );
//} );
jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "scientific-pre": function ( a ) {
        return parseFloat(a);
    },
 
    "scientific-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },
 
    "scientific-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
} );
