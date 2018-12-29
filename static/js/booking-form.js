var selected = [];

$('input[name="destinations[]"]').on('change', function () {
    if (selected.indexOf(this) == -1) {
        selected.push(this);
    } else {
        selected.splice(selected.indexOf(this), 1); // remove using index
    }

    // update UI
    $('.selected-destinations').html('');
    selected.forEach(function (value) {
        $('.selected-destinations').append('<li>' + $(value).next().html() + '</li>');
    });
});

// screening
$('#next').on('click', function (e) {
    e.preventDefault();

    $('.screen-1').fadeOut(function () {
       $('.screen-2').fadeIn();
    });
});

