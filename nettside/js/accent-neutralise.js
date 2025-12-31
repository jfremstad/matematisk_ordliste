/**
 * When searching a table with accented characters, it can be frustrating to have
 * an input such as _Zurich_ not match _Zürich_ in the table (`u !== ü`). This
 * type based search plug-in replaces the built-in string formatter in
 * DataTables with a function that will replace the accented characters
 * with their unaccented counterparts for fast and easy filtering.
 *
 * Note that with the accented characters being replaced, a search input using
 * accented characters will no longer match. The second example below shows
 * how the function can be used to remove accents from the search input as well,
 * to mitigate this problem.
 *
 *  @summary Replace accented characters with unaccented counterparts
 *  @name Accent neutralise
 *  @author Allan Jardine
 *
 *  @example
 *    $(document).ready(function() {
 *        $('#example').dataTable();
 *    } );
 *
 *  @example
 *    $(document).ready(function() {
 *        var table = $('#example').dataTable();
 *
 *        // Remove accented character from search input as well
 *        $('#myInput').keyup( function () {
 *          table
 *            .search(
 *              jQuery.fn.DataTable.ext.type.search.string( this.value )
 *            )
 *            .draw()
 *        } );
 *    } );
 */

(function () {

  function removeAccents(data) {
    return data
      // Normalize to NFD and remove all combining diacritical marks
      .normalize('NFD')
      // Remove all combining diacritical marps
      .replace(/[\u0300-\u036f]/g, '')
      // Replace dashes by hyphens
      .replace(/[–—]/g, '-')
      // Equate 'fram' and 'frem' spelling
      .replace(/fr[ae]m/g, 'fremfram');
  }

  var searchType = jQuery.fn.DataTable.ext.type.search;

  searchType.string = function (data) {
    return !data ?
      '' :
      typeof data === 'string' ?
        removeAccents(data) :
        data;
  };

}());
