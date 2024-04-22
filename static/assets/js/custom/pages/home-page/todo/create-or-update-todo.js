"use strict";

// Class definition
var MCUpdateOrCreateAdmin = function () {
    const handleSubmit = () => {
        let validator;

        // Get elements
        const form = document.getElementById('create-or-update-category-form');
        const submitButton = document.getElementById('create-or-update-category-submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    
                    
                    'todo_title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^(?!\s+$).+/,
                                message: 'Spaces alone are not allowed'
                            }
                        }
                    },
                    
                    'todo_description': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^(?!\s+$).+/,
                                message: 'Spaces alone are not allowed'
                            }
                        }
                    },

                    'status': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'project': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    
                    },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                },
            }
        );

        submitButton.addEventListener('click', (e) => {
            e.preventDefault();

            // Validate form before submit
            if (validator) {
                validator.validate().then((status) => {
                    console.log('validated!');
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    if (status === 'Valid') {
                        // Handle submit button
                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable submit button whilst loading
                        submitButton.disabled = true;
                        submitButton.removeAttribute('data-kt-indicator');
                        // Enable submit button after loading
                        submitButton.disabled = false;

                        // Redirect to customers list page
                        form.submit();
                    } else {
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;
                        Swal.fire({
                            html: "Please Enter Required Fields",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
            }
        });
    };

    // Public methods
    return {
        init: function () {
            handleSubmit();
        }
    };
}();
window.addEventListener('load', function () {
    const loader = document.querySelector('.loader-wrapper');
    loader.style.display = 'none';
});

// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateAdmin.init();
});
