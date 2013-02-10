window.log = -> @console?.log? arguments...

$ ->
  $("#create-bucket").ajaxForm (a,b,c) -> log a, b, c