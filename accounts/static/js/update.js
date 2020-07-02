document.addEventListener("DOMContentLoaded", function () {
  $("#secsession").click(function () {
    $(".tiny.modal").modal('show');
  });
  $(".tiny.modal").modal({ closable: true });
});