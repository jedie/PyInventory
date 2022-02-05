(function ($) {
    'use strict';
    $(function () {
        const form_object = $(form_selector);
        form_object.dirty({
            preventLeaving: true,
            onDirty: function () {
                console.log('form is dirty');
                var dirty_fields = form_object.dirty("showDirtyFields");
                dirty_fields.each(function (index, element) {
                    console.log(index + ' - ' + element.value);
                });
            },
        });
    });
})(django.jQuery);