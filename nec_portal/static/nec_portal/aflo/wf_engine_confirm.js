/*
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

var Aflo = function() {
  var aflo = {};

  aflo.wf_engine_chk_confirm = function(action, form_id) {
    var $action = $(action),
      $modal_parent = $(action).closest('.modal'),
      name_array = [],
      closest_table_id, action_string, name_string,
      help_text, title, body, modal, form;
    if($action.hasClass("disabled")) {
      return;
    }
    modal = horizon.modals.create(
      gettext("Confirm"), gettext("Submit to go on?"),
      gettext("Submit"), gettext("Cancel"));
    modal.addClass('aflo_confirm_dialog');
    modal.modal();
    if($modal_parent.length) {
      var child_backdrop = modal.next('.modal-backdrop');
      // re-arrange z-index for these stacking modal
      child_backdrop.css('z-index', $modal_parent.css('z-index')+10);
      modal.css('z-index', child_backdrop.css('z-index')+10);
    }
    modal.find('.btn-primary').click(function (evt) {
      modal.modal('hide');
      form = $('#' + form_id);
      form.submit();
      horizon.modals.modal_spinner(gettext("Working"));
      return false;
    });
    return modal;
  };

  return aflo;
}

var aflo = new Aflo();
