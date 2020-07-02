document.addEventListener("DOMContentLoaded", function () {
  $(".ui.accordion").accordion();

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
    $(".small.modal").modal('show');
  });
  $(".small.modal").modal({ closable: true });
  console.log("ss")
});