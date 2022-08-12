
$('.login-content [data-toggle="flip"]').click(function () {
    $('.login-box').toggleClass('flipped');
    return false;
});

function onSubmit(token) {
    document.getElementById("login-form").submit();
}
