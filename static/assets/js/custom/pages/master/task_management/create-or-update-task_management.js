"use strict";



// Class definition
var MCUpdateOrCreateSupplier = function () {

    var validator;
    var form;

    var categoryElement, brandElement;

    const handleSubmit = () => {
        

        // Get elements
        form = document.getElementById('create-or-update-task_management-form');
        const submitButton = document.getElementById('create-or-update-task_management-submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    task_name: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    task_description: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    category_name: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    start_date: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    end_date: {
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










    // const handleDropzone = () => {

        
    //     let ProductImageDropzone = new Dropzone("#product_images_dropzone", {
    //         url: `${api_config.product_image_upload_api_url}`,
    //         acceptedFiles: ".jpeg,.jpg,.png",
    //         maxFiles: 5,
    //         paramName: "file",
    //         maxFilesize: 10, // MB
    //         addRemoveLinks: true,
    //         accept: function(file, done) {
    //             done();
    //         },
    //         init: function() {

    //             this.on("maxfilesexceeded", function (data) {
    //                 let res = eval('(' + data.xhr.responseText + ')');
    //             });
    //             this.on("error", function (file, message) {
    //                 //this.removeFile(file);
    //             });
    //             this.on("sending", function(file, xhr, formData){
    //                 formData.append("uuid", `${api_config.uuid}`);
    //                 formData.append("csrfmiddlewaretoken", `${api_config.csrfmiddlewaretoken}`);
    //                 formData.append("files", file);
    //                 formData.append("module", 'product-images');
    //             });
    //             this.on("success", function(file, responseText) {
    //                 if(responseText.status_code == 200)
    //                 {
    //                     //element = file.previewElement.getElementsByTagName('a')?.[0];
    //                     //element.setAttribute('instance_id', responseText.data);
    //                     let childElements = file?.previewElement?.children;
    //                     childElements.forEach(childElement => {
    //                         childElement.setAttribute('instance_id', responseText.data);
    //                         childElement.setAttribute('action_type', 5);
    //                     });
    //                 }
    //             });
    //             this.on('removedfile', function(file) {
    //                 let removeElement = file.previewElement.getElementsByTagName('a')?.[0];
    //                 let instance_id = removeElement.getAttribute('instance_id')
    //                 let action_type = removeElement.getAttribute('action_type')
    //                 $.post(`${api_config.temporary_image_destroy_api_url}`, { id: instance_id, action_type:action_type }, 
    //                     function(data, status, xhr) {
                        
    //                         console.log(data)

    //                     }).done(function() { console.log('Request done!'); })
    //                     .fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });

    //             }); 
    //         }
    //     });



        // ProductImageDropzone.on("addedfile", file => {
        //     let instance_id = file?.instance_id;
        //     let childElements = file?.previewElement?.children;
        //     childElements.forEach(childElement => {
        //         childElement.setAttribute('instance_id', instance_id);
        //         childElement.setAttribute('action_type', 5);
        //     });
        // });
        

    //     $.post(`${api_config.get_product_images_api_url}`, { product_id: `${api_config.product_id}` }, 
    //         function(data, status, xhr) {
    //             if(data.status_code == 200)
    //             {
    //                 $.each(data.data, function (key,value) {
    //                     var mockFile = { name: value.image_name, size: value.size, instance_id: value.id};
    //                     ProductImageDropzone.emit("addedfile", mockFile);
    //                     generateBase64encodedURL(value.image, function(dataURL){ 
    //                         ProductImageDropzone.emit("thumbnail", mockFile, dataURL)
    //                     })
    //                     ProductImageDropzone.emit("complete", mockFile);
                       
    //                 });
                    
    //             }
                

    //         }
    //     ).done(function() { console.log('Request done!'); 
    //     }).fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
    // }





    // const handleSelectOnChnage = () => {
        
    //     if(typeof api_config?.data?.category_id  !== 'undefined')
    //     {
    //         generateSelectOptionElement({pk:api_config?.data?.category_id, api_url : `${api_config.get_category_brands}`, tagElement: brandElement, elementEdit_id: api_config?.data?.brand_id})
    //     }
        
    //     $(categoryElement).on('change', e => {
    //         handleResetSelectOptions({elements: {brandElement}})
    //         generateSelectOptionElement({pk:e.target.value, api_url : `${api_config.get_category_brands}`,tagElement: brandElement})
            
    //     });
    // }


    // const handleResetSelectOptions = ({elements}) => {
    //     let emptyElement = document.createElement('option')
    //     $.each(elements, function (key,element) {
    //         element.innerHTML  = emptyElement
    //         element.dispatchEvent(new Event('change'));
    //     })
    // }

    // const generateSelectOptionElement = ({pk,api_url,tagElement, elementEdit_id = null }) => {
    //     if(pk) {
    //         $.post(api_url, { pk: pk }, function(response, status, xhr) {
    //             if(response?.status_code == 200)
    //             {
    //                 let subOptionElement = document.createElement('option')
    //                 tagElement.appendChild(subOptionElement);
    //                 $.each(response?.data, function (key,value) {
    //                     let subOptionElement = document.createElement('option')
    //                     //
    //                     if(elementEdit_id === value?.id)
    //                     {
    //                         subOptionElement.setAttribute('selected','selected')
    //                     }
    //                     //
    //                     subOptionElement.value = value?.id
    //                     subOptionElement.innerHTML = value?.name
    //                     tagElement.appendChild(subOptionElement);
    //                 });
    //             }
            
    //         }).done(function() { console.log('Request done!'); 
    //         }).fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
    //     }
    // }








    
    // Public methods
    return {
        init: function () {

            categoryElement = document.querySelector('[data-control-select-option="category"]')
            brandElement = document.querySelector('[data-control-select-option="brand"]')

            handleSubmit();
            
            // handleDropzone();
            // handleSelectOnChnage();
            
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateSupplier.init();
});




function generateBase64encodedURL(src, callback){
    var image = new Image();
    image.crossOrigin = 'Anonymous';
    image.onload = function(){
      var canvas = document.createElement('canvas');
      var context = canvas.getContext('2d');
      //canvas.height = this.naturalHeight;
      canvas.height = 140;
      canvas.width = 140;
      //canvas.width = this.naturalWidth;
      context.drawImage(this, 0, 0,140,140);
      var dataURL = canvas.toDataURL('image/jpeg');
      callback(dataURL);
    };
    image.src = src;
}
