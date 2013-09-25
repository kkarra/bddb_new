$(document).ready(function () {
	
    $(".collapse").collapse();

    set_pagination_button_events();
    set_gene_button_events();
    
  //  show_heatmap();
 
    send_email();
    close_tab();

    //for gene search
    $("#geneSearch").click(function(e) {

	    e.preventDefault();
	    var queryGenes = $("#geneQuery").val();
	    var genesArray = queryGenes.split(",");
	    // make sure a species button is clicked (multiple name error)
	    //open a single gene page if there is
	    // only one gene to query
	    if (genesArray.length == 1) {
		var gene = genesArray[0];
		
		openGenePage(gene);

	    } else {
	    	
		$.get("search/filter/",
		      {genes: queryGenes}, 
		      function(data) {
			  $("#summary").replaceWith(data);
			  set_gene_button_events();
			  set_pagination_button_events();
			  show_heatmap();
			  close_tab();
		    });
	    }

	});
		
    // for toggle button //

    $("#allSpecies").click(function() {
	    $(".speciesBut").toggleClass("active");
	});

    // for filtering. if any species is selected...find
    // all active ones//  

       $(".speciesBut").click(function(e){
    	    e.preventDefault();
	    filter_data(1);
    	});

       $(".tissueBox:checkbox").change(function(e) {
	       e.preventDefault();
	       filter_data(1);
	   });
    		
       $(".methodBox:checkbox").change(function(e) {
	       e.preventDefault();
	       filter_data(1);
	   });

}); // ends document ready


/*$(document).ready(function () {
	    	
		$.get("search_new/",
		      {tissues: tissueList}, 
		      function(data) {
			  $("#summary").replaceWith(data);

		    });
		    
}); // ends document ready
*/
function changePage(pge) {   
    // alert("new Page "+ pge); 
    $.get("search/summary/"+ pge, function (data) {
	    $("#summary").replaceWith(data);
	set_pagination_button_events();
	set_gene_button_events();
	show_heatmap();
	close_tab();
    });
}

function openGenePage(gene, geneId) {
    if (typeof geneId == 'undefined'){ geneId = gene; }
       alert("gene and id:"+ gene + "," + geneId);

    $("#results-tabs li").removeClass("active");
    $("#results-content div").removeClass("active");
  
    $("#results-tabs").append($('<li class="active"><a href="#search' + geneId + '"data-toggle="tab">' + gene +'<sup>  <i class=\'icon-remove closetab\' id=\'close-'+geneId +'\'></i></sup></a></li>'));
    
    $.get("search/"+geneId, function(data) {
       $("#results-content").append(data)
		
     //  $("#heatMapInfo").ajaxSuccess(function () { 
	 // var cXGeneData;
	 // var cXGeneConfig;  
	 // var cXGeneDataJson;
	 // var cXGeneConfigJson;
	 // var canvasId;
	  //cXGeneData = $("input#geneMapData"+geneId).val();
     // cXGeneConfig = $("input#geneMapConfig"+geneId).val();
  
	//  cXGeneDataJson = JSON.parse(cXGeneData);
	//  cXGeneConfigJson = JSON.parse(cXGeneConfig);
 
	 // canvasId = "peakCanvas"+geneId;

       //	  var cX=new CanvasXpress(canvasId, cXGeneDataJson, cXGeneConfigJson);          });
       set_gene_button_events();
       close_tab()
        });
};

function filter_data(page) {
        var species = new Array();
	    var displayArr = new Array();
	    var page = page;

    	    if (($('.speciesBut.active').text()).length > 0) {
    		$('button.speciesBut.active').each(function(){
    			species.push($(this).attr('data-value'));
			displayArr.push($(this).attr('text'));
    		    })
    	    }
    	    // hack to take into acct twitter-boostrap 'active' delay
    	    if ($(this).hasClass('active')){
    		species.splice(species.indexOf($(this).attr('data-value')), 1);
    		displayArr.splice(displayArr.indexOf($(this).attr('text')), 1);
    	    } else {	
    		species.push($(this).attr('data-value'));
		displayArr.push($(this).attr('text'));
    	    }
    
    	    var tissues = $(".tissueBox:checkbox:checked").map(function(){
    		    return $(this).val()}).get();
    	    var methods = $(".methodBox:checkbox:checked").map(function(){
    		    return $(this).val()}).get();
	    
	    displayArr.push($(".tissueBox:checkbox:checked").map(function(){
			return $(this).attr('id')}).get());
	    displayArr.push($(".methodBox:checkbox:checked").map(function(){
			return $(this).attr('id')}).get());
	    
	    var search_terms = displayArr.join();
    	    replace_with_filtered_data(species, tissues, methods, page, search_terms);
}


function replace_with_filtered_data(speciesList, tissuesList, methodsList, curr_pg, display) {
    // species -- species_id
    // tissues -- anatomy_ontology.uberon_id; also datasets.uberon_id
    // methods --  datasets.method_id
    species = speciesList.join("|") || "no species filter";
    tissues = tissuesList.join("|") || "no tissue filter";
    methods = methodsList.join("|") || "no method filter";
    page = curr_pg || 1;

    $.get('/search/filter/',{
	        species: species,
		tissues: tissues,
		methods: methods,
		page: curr_pg,
		display: display
		}, function(data) {
	    //  alert(data);
	    $('#summary').replaceWith(data);
	    set_gene_button_events();
	    set_pagination_button_events();
	    show_heatmap();
	    close_tab();
	});
    
}

function download_button_events () {
    $("#download").click(function(e) {
	    e.preventDefault();
	    data = $("input#mapData").val();
	    window.location.href = '/download', {json: data};
	});
}

function set_pagination_button_events() {

$(".pageBut").click(function(e) {
	    e.preventDefault();
	    var page_val = $(this).attr('value');
	    //    alert("Page button clicked: ", page_val)
	    if ($("div.filtered").length != 0) {
		filter_data(page_val);
	    } else {
		changePage(page_val);
	    }
    });
}

function set_gene_button_events() {
    $(".geneButton").click(function (e) {
	    e.preventDefault();
	    var gene;
	    var geneId;
	    gene = $(this).attr('value');
	    geneId = $(this).attr('id');
	
	    openGenePage(gene,geneId);
	    close_tab();
    });
}

function show_heatmap() {
     if ($("input#mapData").val() != ""){

	  var cXData = $("input#mapData").val();
          var cXConfig = $("input#mapConfig").val();
	  var gene;
	  var geneId;

	  var cXEvent = {click: function(o) { // to open new gene tab when clicked
		  var smpVal = o.display; 
		  openGenePage(o.display);
	     }}; 
	  var cXDataJson = JSON.parse(cXData);
	  var cXConfigJson = JSON.parse(cXConfig);
	  
	  // alert("event: "+cXEvent);
	  
	  var cX=new CanvasXpress("manyPeaksCanvas", cXDataJson, cXConfigJson, cXEvent); 
     };
}

function send_email() {

    $('#upload').click(function() {
	    var name= $('input#name').val();
	    var email=$('input#contact').val();
	    var filename=$('input#file').val();
	    var caller = $('input#peakcaller').val();
	    
	    var ipinput;
	    
	    if ($('input#ipinput1').attr('checked')) {
	    		ipinput = $('input#ipinput1').val();
	    } 
	 	if ($('input#ipinput2').attr('checked')) {
	    	ipinput = $('input#ipinput2').val();
	    }

	    var info = $('input#details').val();

	    var submitData = "Name="+ name + "& email=" + email + "&file=" + filename + "&peakcaller=" + caller + 
	    	"&ipinput=" + ipinput +"&details=" + info;

	    $.ajax({
		    type: "POST",
			url: "/submitted",
			data: submitData,
			success: function() {
			alert("Thank you for your submission");
		    }
		});
	});
}

function close_tab() {
    $(".closetab").click(function() {
	    var id = $(this).attr('id');
	    var idArr = id.split("-");
	    $("#results-tabs li.active").hide();
	    $("#results-content div").removeClass("active");
	    $("#summary").addClass('active');
	    $("#search"+idArr[1]).hide();
	});
}