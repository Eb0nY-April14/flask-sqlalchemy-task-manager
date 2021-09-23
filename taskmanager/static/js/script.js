/* COPY THIS JS CODE BELOW FROM THE Materialize WEBSITE FOR Initialisation 
& CUSTOMISE IT BY RENAMING THE VARIABLES TO SUIT OUR PURPOSE AS DONE BELOW */
/*document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, options);
  }); */

/* CUSTOMISED JS CODE: TO INITIALISE ALL OUR ELEMENTS VIA JAVASCRIPT */
document.addEventListener('DOMContentLoaded', function() {
    // sidenav initialisation
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

    // datepicker initialisation 
    let datepicker = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datepicker, {
        format: "dd mmmm, yyyy",
        i18n: {done: "Select"}
    });

    // select initialisation 
    let selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);

    // collapsible elements initialisation
    let collapsibles = document.querySelectorAll('.collapsible');
    M.Collapsible.init(collapsibles);
});