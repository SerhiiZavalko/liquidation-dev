odoo.define('web.search.panel', function (require) {
  'use strict';

  const SearchPanel = require('web/static/src/js/views/search_panel.js')
  SearchPanel.patch('OwlSearchPanel.SearchPancel', (T) => {
    class ControlPanelPatched extends T {
      click_search_panel () {
        if ($('div').hasClass('search_panel_o_hidden')) {
          $('.o_search_panel').removeClass('search_panel_o_hidden')
          $('#o_search_panel_control')
            .removeClass('o_search_panel_control_left')
            .addClass('o_search_panel_control')
          $('#o_search_panel_control')
            .removeClass('fa-angle-double-right')
            .addClass('fa-angle-double-left')
        } else {
          $('.o_search_panel').addClass('search_panel_o_hidden')
          $('#o_search_panel_control')
            .removeClass('o_search_panel_control')
            .addClass('o_search_panel_control_left')
          $('#o_search_panel_control')
            .removeClass('fa-angle-double-left')
            .addClass('fa-angle-double-right')
        }
      }
    }

    return ControlPanelPatched
  })
})
