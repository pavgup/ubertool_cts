$(document).ready(function() {

    uberNavTabs(
        ["Chemical", "ReactionPathSim", "ChemCalcs", "ReactionRateCalc"],
        {   "isSubTabs":true,
        	"Chemical": [".tab_chemicalButtons"] }
    );

    $('#chemEditDraw_button').click(function() {
    	$('#chemEditDraw').show();
    	// $('#chemEditLookup').hide();
    });

    $('#chemEditLookup_button').click(function() {
    	$('#chemEditLookup').show();
    	// $('#chemEditDraw').hide();
    });
    
    // ####### UNCOMMENT AFTER TESTING ###################

    // Main tables
    $('#cts_reaction_paths').show();
    $('#oecd_selection').hide();
    $('#ftt_selection').hide();
    $('#health_selection').hide();
    $('#cts_reaction_sys').hide();
    $('#respiration_tbl').hide();
    $('#cts_reaction_libs').hide();

    //Respiration table contents
    $('#aerobic_picks').hide();
    $('#anaerobic_picks').hide();

    //Disable checkboxes (only enable for "Reaction Pathway" selection)
    $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', true);

    $("input[name='reaction_paths']").change(function() {
        if ($(this).val() == "0") {
            //If "Reaction System" is selected
            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').hide();
        }

        else if ($(this).val() == "1") {
            //If "OECD Guidelines" is checked..
            $('#cts_reaction_paths').show();
            $('#oecd_selection').show();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').hide();
        }

        else if ($(this).val() == "2") {
            //Show Reaction Library with "Reaction Library" checked
            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').show();

            //Set Reaction Libraries table...
            $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', false);

            $('#id_abiotic_hydrolysis').prop('checked', false);
            $('#id_aerobic_biodegradation').prop('checked', false);
            $('#id_photolysis').prop('checked', false);
            $('#id_abiotic_reduction').prop('checked', false);
            $('#id_anaerobic_biodegrad').prop('checked', false);
            $('#id_mamm_metabolism').prop('checked', false);
        }
    });

    $("input[name='reaction_system']").change(function() {
        if ($(this).val() == "0") {
            //If "Environmental" is selected..
            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').show();
            $('#cts_reaction_libs').hide();
        }
        else if ($(this).val() == "1") {
            //Show Reaction Library with "Mammalian" selected
            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').show();

            //Set what's checkable in Reaction Libraries table
             $('#id_mamm_metabolism').prop('checked', true);
        }
    });

    $("input[name='respiration']").change(function() {

        //Main tables
        $('#cts_reaction_paths').show();
        $('#oecd_selection').hide();
        $('#ftt_selection').hide();
        $('#health_selection').hide();
        $('#cts_reaction_sys').show();
        $('#respiration_tbl').show();
        $('#cts_reaction_libs').show();

        if ($(this).val() == "0") {
            //Display aerobic column...
            $('#aerobic_picks').show();
            $('#anaerobic_picks').hide();

            //Set Reaction Libraries ...
            $('#id_abiotic_hydrolysis').prop('checked', true);
            $('#id_aerobic_biodegradation').prop('checked', true);
            $('#id_photolysis').prop('checked', true);
            $('#id_abiotic_reduction').prop('checked', true);
            $('#id_anaerobic_biodegrad').prop('checked', false);
            $('#id_mamm_metabolism').prop('checked', false);

        }
        else if ($(this).val() == "1") {
            //Display anaerobic column...
            $('#aerobic_picks').hide();
            $('#anaerobic_picks').show();

            //Set Reaction Libraries table...
            $('#id_abiotic_hydrolysis').prop('checked', true);
            $('#id_aerobic_biodegradation').prop('checked', false);
            $('#id_photolysis').prop('checked', false);
            $('#id_abiotic_reduction').prop('checked', true);
            $('#id_anaerobic_biodegrad').prop('checked', true);
            $('#id_mamm_metabolism').prop('checked', false);
        }
    });

    $("input[name='oecd_selection']").change(function() {

        //FTT content columns
        $('#labAbioTrans_picks').hide();
        $('#transWaterSoil_picks').hide();
        $('#transChemSpec_picks').hide();

        if ($(this).val() == "0") {
            //If FTT is selected

            //Main tables
            $('#cts_reaction_paths').show();
            $('#oecd_selection').show();
            $('#ftt_selection').show();
            $('#health_selection').hide();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').hide();
        }
        else if ($(this).val() == "1") {
            //If "Health Effects" is selected

            //Main tables
            $('#cts_reaction_paths').show();
            $('#oecd_selection').show();
            $('#ftt_selection').hide();
            $('#health_selection').show();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').hide();

            //Select only option in Health Effects
            $('#id_specialStudies_selection_0').prop('checked', true);
        }
    });

    $("input[name='ftt_selection']").change(function() {

        //Main tables
        $('#cts_reaction_paths').show();
        $('#oecd_selection').show();
        $('#ftt_selection').show();
        $('#health_selection').hide();
        $('#cts_reaction_sys').hide();
        $('#respiration_tbl').hide();
        $('#cts_reaction_libs').hide();

        if ($(this).val() == "0") {
            //If  Laboratory Abiotic Transformation Guidelines is selected

            //Display LATG column
            $('#labAbioTrans_picks').show();
            $('#transWaterSoil_picks').hide();
            $('#transChemSpec_picks').hide();
            
        }
        else if ($(this).val() == "1") {
            //If Transformation in Water and Soil Test Guidelines is selected

            //Display TWSTG column
            $('#labAbioTrans_picks').hide();
            $('#transWaterSoil_picks').show();
            $('#transChemSpec_picks').hide();
        }
        else if ($(this).val() == "2") {
            //If Transformation Chemcial-Specific Test Guidelines is selected

            //Display TCSTG column
            $('#labAbioTrans_picks').hide();
            $('#transWaterSoil_picks').hide();
            $('#transChemSpec_picks').show();
        }
    });

    // #######################################################

});