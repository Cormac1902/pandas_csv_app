$('#file').on('change',function(){
    $(this).next('.custom-file-label').html(document.getElementById("file").files[0].name);
})

$('select').selectpicker();