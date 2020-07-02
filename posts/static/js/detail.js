document.addEventListener("DOMContentLoaded", function () {
  $("#delete").click(function() {
    $(".tiny.modal").modal('show');
  });
  $(".tiny.modal").modal({ closable: true });

  const current_url = window.location.href;
  $("#current_url").attr('value', current_url);
  
  $(".url_copy").click(function() {
    $("#current_url").css({ 'display': 'block' }).select();
    document.execCommand("Copy");
    $("#current_url").css({ 'display': 'none' });
    alert("주소가 복사되었습니다.")
    return false;
  });

  $('.author').click(function() {
    $('#note').empty();
    $('.note.coupled.modal').modal({
      allowMultiple: false
    });
    $('.note.second.modal').modal('attach events', '.small.note.first.modal .positive.button');
    $('.small.note.first.modal').modal('show');
  });

  $('.email').click(function () {
    $("#subject").empty();
    $('#mail').empty();
    $('.mail.coupled.modal').modal({
      allowMultiple: false
    });
    $('.mail.second.modal').modal('attach events', '.small.mail.first.modal .positive.button');
    $('.small.mail.first.modal').modal('show');
  });
});