window.log = -> @console?.log? arguments...

$ ->
  $alertError = $("#alert-error")
  $alertError.find(".close").click -> $alertError.fadeOut()

  if localStorage["aws-key"] && localStorage["aws-secret"]
    $("#aws-key").val(localStorage["aws-key"])
    $("#aws-secret").val(localStorage["aws-secret"])

  $("#create-bucket").submit (e) ->
    e.preventDefault()

    $form = $(@)
    $btn = $form.find("input[type=submit]")

    $alertError.hide()
    $btn.button 'loading'

    $form.ajaxSubmit (response) ->
      $btn.button 'reset'

      if response.status
        b = response.bucket
        $("#new-bucket-name").text(b.bucket_name)
        $("#new-aws-key").text(b.aws_key)
        $("#new-aws-secret").text(b.aws_secret)

        $('#success-modal').modal
          show: true
          backdrop: false
      else
        $alertError.fadeIn().find('.alert-message').text(response.message)

      # Store creds if they want
      if $("#save-creds:checked").length and response.status
        # TODO: check for browser support
        localStorage["aws-key"] = $("#aws-key").val()
        localStorage["aws-secret"] = $("#aws-secret").val()
      else if not $("#save-creds:checked").length
        localStorage.removeItem "aws-key"
        localStorage.removeItem "aws-secret"

