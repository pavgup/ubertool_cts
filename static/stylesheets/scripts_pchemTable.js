$(document).ready(function() {    

    //Initialize all checkboxes to be unchecked:
    $("input:checkbox").prop('checked', false);

    //Start with the cells containing classes ChemCalcs_available or ChemCalcs_unavailable;
    //Make them slightly transparent, then darken a column that's selected.

    $('.ChemCalcs_available').fadeTo(0, 0.75);  
    $('.ChemCalcs_unavailable').fadeTo(0, 0.75);


    //######## From scripts_pchemprop.js ###################
    var isAllChecked_ChemCalcs = 1;

    var noOfInput_ChemCalcs = []
    $('#tab_ChemCalcs').find('input').push(noOfInput_ChemCalcs);
    noOfInput_ChemCalcs = noOfInput_ChemCalcs.length;
    var noOfInput_ChemCalcs = $(".tab_ChemCalcs input").length -1;

    var isChecked_ChemCalcs = [];
    $('#id_all').click(function() {
        if ($('#id_all').is(":checked")) {
            $('.chemaxon').fadeTo(0, 1);
            $('.epi').fadeTo(0, 1);
            $('.test').fadeTo(0, 1);
            $('.sparc').fadeTo(0, 1);
            $('.measured').fadeTo(0, 1);
        } else {
            $('.chemaxon').fadeTo(0, 0.75);
            $('.epi').fadeTo(0, 0.75);
            $('.test').fadeTo(0, 0.75);
            $('.sparc').fadeTo(0, 0.75);
            $('.measured').fadeTo(0, 0.75);
        }
    });        
/*
    $("#id_all").click(function() {
<<<<<<< HEAD
        switch(isAllChecked_ChemCalcs) {
=======
         switch(isAllChecked_ChemCalcs) {
>>>>>>> pavan
            case 1:
                isAllChecked_ChemCalcs = 0;
                $(".chemprop input:checkbox").prop( "checked", true );
                console.log('Set checked');
                break;
            case 0:
                $(".chemprop input:checkbox").prop( "checked", false );
                isAllChecked_ChemCalcs = 1;
                console.log('Set unchecked');
                break;
            default:
                console.log('JavaScript Error');
        }
    });*/
    //#########################################################


    //Highlight column of selected datasource:
    $('#id_chemaxon_select').click(function() {
      
        if ($('#id_chemaxon_select').is(":checked"))
        {
         
            $('.chemaxon').fadeTo(0, 1);
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/MP", dataType: "json"}).done(function(val) { $('#id_water_sol_ChemAxon').html(val.TEST.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/BP", dataType: "json"}).done(function(val) { $('#id_ionization_con_ChemAxon').html(val.TEST.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/VP", dataType: "json"}).done(function(val) { $('#id_kow_no_ph_ChemAxon').html(val.TEST.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/WS", dataType: "json"}).done(function(val) { $('#id_kow_ChemAxon').html(val.TEST.toPrecision(4)) } )
        }
        else
        {
            
            $('.chemaxon').fadeTo(0, 0.75);  
        }

    });
    $('#id_epi_select').click(function() {
      
        if ($('#id_epi_select').is(":checked"))
        {
         
            $('.epi').fadeTo(0, 1);
        }
        else
        {
            
            $('.epi').fadeTo(0, 0.75);  
        }

    });
    $('#id_measured_select').click(function() {
      
        if ($('#id_measured_select').is(":checked"))
        {
            // $(this).closest('tr').switchClass('pchem_unchecked_col', 'pchem_checked_col');
            $('.measured').fadeTo(0, 1);
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/MP/MEASURED", dataType: "json"}).done(function(val) { $('#id_melting_point_MEASURED').html(val.MEASURED.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/BP/MEASURED", dataType: "json"}).done(function(val) { $('#id_boiling_point_MEASURED').html(val.MEASURED.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/WS/MEASURED", dataType: "json"}).done(function(val) { $('#id_water_sol_MEASURED').html(val.MEASURED.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/VP/MEASURED", dataType: "json"}).done(function(val) { $('#id_vapor_press_MEASURED').html(val.MEASURED.toPrecision(4)) } )
        }
        else
        {
            // $(this).closest('tr').toggleClass('pchem_unchecked_col', 'pchem_unchecked_col'); 
            $('.measured').fadeTo(0, 0.75);  
        }

    });
      
    $('#id_test_select').click(function() {
      
        if ($('#id_test_select').is(":checked"))
        {
            $('.test').fadeTo(0, 1);
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/MP", dataType: "json"}).done(function(val) { $('#id_melting_point_TEST').html(val.TEST.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/BP", dataType: "json"}).done(function(val) { $('#id_boiling_point_TEST').html(val.TEST.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/WS", dataType: "json"}).done(function(val) { $('#id_water_sol_TEST').html(val.TEST.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/VP", dataType: "json"}).done(function(val) { $('#id_vapor_press_TEST').html(val.TEST.toPrecision(4)) } )
            $.ajax({type: "GET", url: "/test_cts/api/TEST/"+$('#molecule').val()+"/MLOGP", dataType: "json"}).done(function(val) { $('#id_kow_no_ph_TEST').html(val.MLOGP.toPrecision(4)) } )
        }
        else
        {
            
            $('.test').fadeTo(0, 0.75);  
        }

    });
    $('#id_sparc_select').click(function() {
      
        if ($('#id_sparc_select').is(":checked"))
        {
         
            $('.sparc').fadeTo(0, 1);
        }
        else
        {
            
            $('.sparc').fadeTo(0, 0.75);  
        }

    });
    $('#id_melting_point').click(function() {
        if ($('#id_melting_point').is(":checked")) {
            $('.id_melting_point').fadeTo(0, 1);
        } else {
            $('.id_melting_point').fadeTo(0, 0.75);
        }
    });

    $('#id_boiling_point').click(function() {
        if ($('#id_boiling_point').is(":checked")) {
            $('.id_boiling_point').fadeTo(0, 1);
        } else {
            $('.id_boiling_point').fadeTo(0, 0.75);
        }
    });

    $('#id_water_sol').click(function() {
        if ($('#id_water_sol').is(":checked")) {
            $('.id_water_sol').fadeTo(0, 1);
        } else {
            $('.id_water_sol').fadeTo(0, 0.75);
        }
    });

    $('#id_vapor_press').click(function() {
        if ($('#id_vapor_press').is(":checked")) {
            $('.id_vapor_press').fadeTo(0, 1);
        } else {
            $('.id_vapor_press').fadeTo(0, 0.75);
        }
    });

    $('#id_mol_diss').click(function() {
        if ($('#id_mol_diss').is(":checked")) {
            $('.id_mol_diss').fadeTo(0, 1);
        } else {
            $('.id_mol_diss').fadeTo(0, 0.75);
        }
    });

    $('#id_ionization_con').click(function() {
        if ($('#id_ionization_con').is(":checked")) {
            $('.id_ionization_con').fadeTo(0, 1);
        } else {
            $('.id_ionization_con').fadeTo(0, 0.75);
        }
    });

    $('#id_henrys_law_con').click(function() {
        if ($('#id_henrys_law_con').is(":checked")) {
            $('.id_henrys_law_con').fadeTo(0, 1);
        } else {
            $('.id_henrys_law_con').fadeTo(0, 0.75);
        }
    });

    $('#id_kow_no_ph').click(function() {
        if ($('#id_kow_no_ph').is(":checked")) {
            $('.id_kow_no_ph').fadeTo(0, 1);
        } else {
            $('.id_kow_no_ph').fadeTo(0, 0.75);
        }
    });

    $('#id_kow_wph').click(function() {
        if ($('#id_kow_wph').is(":checked")) {
            $('.id_kow_wph').fadeTo(0, 1);
        } else {
            $('.id_kow_wph').fadeTo(0, 0.75);
        }
    });
});
