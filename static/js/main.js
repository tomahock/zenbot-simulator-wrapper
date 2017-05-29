/**
 * Created by tomahock on 26/05/17.
 */
$(function () {
    $('.selector-select').on('change', function (e) {
        var selector = this.value;
        var result = $.grep(markersJson, function (f) {
            return f.selector == selector;
        })[0];

        var from = moment.unix(result.from);
        var to = moment.unix(result.to);

        info = '<div class="alert alert-info"><p>From: ' + from.format("DD/MM/YYYY") + '</p>' +
            '<p>To: ' + to.format("DD/MM/YYYY") + '</p>' +
            '<p>Max Days:' + to.diff(from, 'days') + '</p></div>';

        $('.selectorInfo').html(info);
    });
});
