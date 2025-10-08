$('.show-alert-delete-box').click(function (event) {
    var form = $(this).closest("form");
    var name = $(this).data("name");
    event.preventDefault();
    swal({
        title: "Are You Sure Want To Delete ? ",
        icon: "warning",
        type: "warning",
        buttons: ["Cancel", "Yes"],
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: "{{ __('site.yes')}}, delete it!"
    }).then((willDelete) => {
        if (willDelete) {
            form.submit();
        }
    });
});