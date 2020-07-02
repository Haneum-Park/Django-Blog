document.addEventListener("DOMContentLoaded", function () {
  $('.ui.search.dropdown').dropdown();
  $('#reply').click(function () {
    const reply_username = $(this).attr("data-from");

    $("#fromed_reply").text(reply_username);
    document.getElementById("note").textContent = "";
    $('.note.coupled.modal').modal({
      allowMultiple: false
    });
    $('.note.second.modal').modal('attach events', '.small.note.first.modal .positive.button');
    $('.small.note.first.modal').modal('show');
  });
});