"use strict";



// Class definition
var MCUpdateOrCreateRoles = function () {

    var validator;
    var form;


    const handleSubmit = () => {
        

        // Get elements
        form = document.getElementById('create-or-update-role-form');
        const submitButton = document.getElementById('create-or-update-role-submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    role_name: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    permissions: {
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
                }
            }
        );


        submitButton.addEventListener('click', e => {



            const permissionIdsOutput = document.querySelector(`[data-control-permissions="id"]`)

            var permissionIds = []

            let selected_nodes = $('#_jstree_checkable').jstree().get_selected(true)

            selected_nodes.forEach(d => {
                if(typeof d.a_attr.permission_id != 'undefined')
                {
                    permissionIds.push(d.a_attr.permission_id)
                }
            })

            permissionIdsOutput.value = JSON.stringify(permissionIds)


            e.preventDefault();

            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    
                    console.log('validated!');
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    if (status == 'Valid') {

                        // Handle submit button
                        e.preventDefault();

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
                            html: "Please enter the required fields",
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



        


    }






    const handlePermissionTree = () => {


        $.post(`${api_config.generate_permission_tree}`, {role_id :`${api_config.role_id}`}, function(data, status, xhr) {

            console.log(data.data)
            if(data.status_code == 200)
            {
                $('#_jstree_checkable').jstree({
                    'plugins': ["wholerow", "checkbox", "types","changed"],
                    'core': {
                        "themes" : {
                            "responsive": false
                        },
                        'data': data.data
                    },
                    "types" : {
                        "default" : {
                            "icon" : "fa fa-folder text-primary"
                        },
                        "file" : {
                            "icon" : "fa fa-file text-primary"
                        }
                    },
                });
                
            }


        }).done(function() { console.log('Request done!'); })
        .fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });



        
    }





    
    // Public methods
    return {
        init: function () {
            handleSubmit();

            handlePermissionTree();
            
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateRoles.init();
});




