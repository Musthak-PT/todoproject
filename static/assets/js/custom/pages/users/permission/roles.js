"use strict";

// Class definition
var DatatablesAndCRUDOperationServerSide = function() {


    // start datatable and deleteation section

    // Shared variables
    var table;
    var dt;

    // Private functions
    var initDatatable = function() {
        
        dt = $("#roles-datatable").DataTable({
            searchDelay: 500,
            serverSide: true,
            responsive: true,
            processing: true,
            order: [
                [0, 'desc']
            ],
            select: {
                style: 'multi',
                selector: 'td:first-child input[type="checkbox"]',
                className: 'row-selected'
            },
            ajax: {
                method: "POST",
                url: `${api_config.datatable}`,
                data: {
                    'csrfmiddlewaretoken': `${api_config.csrfmiddlewaretoken}`,
                },
            },
            columns: [
                {data: 'id'},
                {data: 'name'},
                {data: 'permissions'},
                {data: 'id'}, 
            ],
            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data) {
                        return `
                            <div class="form-check form-check-sm form-check-custom form-check-solid">
                                <input class="form-check-input checkbox-input-id" type="checkbox" value="${data}" />
                            </div>`;
                    }
                },

                {
                    targets: -1,
                    data: null,
                    orderable: false,
                    className: 'text-end',
                    render: function (data, type, row) {
                        let edit_url = api_config.edit_url.replace('0', row.encrypt_id.toString());
                        var perm_value = document.getElementById("check_perm").value
                        if(perm_value){
                            return `
                                <div class="d-flex justify-content-end flex-shrink-0">
                                    <a href="${edit_url}" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                                    <span class="svg-icon svg-icon-3">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                            <path opacity="0.3" d="M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988 17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355 21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099 14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449 21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z" fill="currentColor" />
                                            <path d="M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744 21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799 20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z" fill="currentColor" />
                                        </svg>
                                    </span>
                                    </a>
                                    <a href="javascript:void(0)" data-id=${row.id} data-roles-table-filter="delete_row" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm">
                                        <span class="svg-icon svg-icon-3">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                                <path d="M5 9C5 8.44772 5.44772 8 6 8H18C18.5523 8 19 8.44772 19 9V18C19 19.6569 17.6569 21 16 21H8C6.34315 21 5 19.6569 5 18V9Z" fill="currentColor" />
                                                <path opacity="0.5" d="M5 5C5 4.44772 5.44772 4 6 4H18C18.5523 4 19 4.44772 19 5V5C19 5.55228 18.5523 6 18 6H6C5.44772 6 5 5.55228 5 5V5Z" fill="currentColor" />
                                                <path opacity="0.5" d="M9 4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V4H9V4Z" fill="currentColor" />
                                            </svg>
                                        </span>
                                    </a>
                                </div> `;
                        
                                }else{
                                    return `<div class="d-flex justify-content-end flex-shrink-0">
                                            <a href="${edit_url}" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                                            <span class="svg-icon svg-icon-3">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                                    <path opacity="0.3" d="M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988 17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355 21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099 14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449 21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z" fill="currentColor" />
                                                    <path d="M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744 21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799 20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z" fill="currentColor" />
                                                </svg>
                                            </span>
                                            </a>
                                        </div>`;
                                }        
                    },
                },
            ],
                    // Add data-filter attribute
                    
            drawCallback: function(settings) {},
            fnRowCallback: function (nRow, aData, iDisplayIndex) {
                var info = $(this).DataTable().page.info();
                $("td:nth-child(1)", nRow).html(info.start + iDisplayIndex + 1);
                return nRow;
            },
        
            drawCallback: function(settings) {},
            createdRow: function(row, data, dataIndex) {
                $(row).find('td:eq(4)').attr('data-filter', data.CreditCardType);
            }
        });

        table = dt.$;
        
        // Re-init functions on every table re-draw -- more info: https://datatables.net/reference/event/draw
        dt.on('draw', function() {
            
            
            initToggleToolbar();
            toggleToolbars();
            handleDeleteRows(); 
            KTMenu.createInstances();
        });
    }

    // Search Datatable --- official docs reference: https://datatables.net/reference/api/search()
    var handleSearchDatatable = function() {
        const filterSearch = document.querySelector('[data-roles-table-filter="search"]');
        filterSearch.addEventListener('keyup', function(e) {
            dt.search(e.target.value).draw();
        });
    }

    


    var handleDeleteRows = () => {
        // Select all delete buttons
        const deleteButtons = document.querySelectorAll('[data-roles-table-filter="delete_row"]');

        deleteButtons.forEach(d => {
            // Delete button on click
            d.addEventListener('click', function(e) {

                const destroyRecordIds = [$(this).data('id')];
                e.preventDefault();
                // Select parent row
                const parent = e.target.closest('tr');
                const userName = parent.querySelectorAll('td')[1].innerText;
                // Get customer name
                //     // SweetAlert2 pop up --- official docs reference: https://sweetalert2.github.io/
                Swal.fire({
                    text: "Are you sure you want to delete " + userName + "?",
                    icon: "warning",
                    showCancelButton: true,
                    buttonsStyling: false,
                    confirmButtonText: "Yes, delete!",
                    cancelButtonText: "No, cancel",
                    customClass: {
                        confirmButton: "btn fw-bold btn-danger",
                        cancelButton: "btn fw-bold btn-success"
                    }
                }).then(function(result) {
                    if (result.value) {
                        $.post(`${api_config.delete_records}`, { ids: destroyRecordIds }, function(data, status, xhr) {
                            if (data.status_code == 200) {
                                Swal.fire({
                                    text: "You have deleted !.",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                }).then(function() {
                                    // delete row data from server and re-draw datatable
                                    dt.draw();
                                });

                            } else {
                                Swal.fire({
                                    text: "Something went wrong.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                });
                            }

                        }, 'json').done(function() {
                            console.log('Request done!');
                        }).fail(function(jqxhr, settings, ex) {
                            console.log('failed, ' + ex);
                            Swal.fire({
                                text: "Something went wrong.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            });
                        });

                    } 
                });
            })
        });
    }


    // // Init toggle toolbar
    var initToggleToolbar = function() {
        // Toggle selected action toolbar
        // Select all checkboxes
        const container = document.querySelector('#roles-datatable');
        const checkboxes = container.querySelectorAll('[type="checkbox"]');

        // // Select elements
        // const deleteSelected = document.querySelector('[data-roles-table-select="delete_selected"]');

        // Toggle delete selected toolbar
        checkboxes.forEach(c => {
            // Checkbox on click event
            c.addEventListener('click', function() {
                setTimeout(function() {
                    toggleToolbars();
                }, 50);
            });
        });

        // Deleted selected rows
        // deleteSelected.addEventListener('click', function() {

        //     const row_ids = []
        //     $(".checkbox-input-id:checkbox:checked").each(function() {
        //         row_ids.push($(this).val());
        //     });

        //     Swal.fire({
        //         text: "Are you sure you want to delete selected records?",
        //         icon: "warning",
        //         showCancelButton: true,
        //         buttonsStyling: false,
        //         showLoaderOnConfirm: true,
        //         confirmButtonText: "Yes, delete!",
        //         cancelButtonText: "No, cancel",
        //         customClass: {
        //             confirmButton: "btn fw-bold btn-danger",
        //             cancelButton: "btn fw-bold btn-active-light-primary"
        //         },
        //     }).then(function(result) {
        //         if (result.value) {

        //             $.post(`${api_config.delete_records}`, { ids: row_ids }, function(data, status, xhr) {

        //                 if (data.status = 200) {
        //                     Swal.fire({
        //                         text: "You have deleted SuccessFully records!.",
        //                         icon: "success",
        //                         buttonsStyling: false,
        //                         confirmButtonText: "Ok, got it!",
        //                         customClass: {
        //                             confirmButton: "btn fw-bold btn-primary",
        //                         }
        //                     }).then(function() {
        //                         // delete row data from server and re-draw datatable
        //                         dt.draw();
        //                         const headerCheckbox = container.querySelectorAll('[type="checkbox"]')[0];
        //                         headerCheckbox.checked = false;
        //                     });

        //                 } else {
        //                     Swal.fire({
        //                         text: "Something went wrong.",
        //                         icon: "error",
        //                         buttonsStyling: false,
        //                         confirmButtonText: "Ok, got it!",
        //                         customClass: {
        //                             confirmButton: "btn fw-bold btn-primary",
        //                         }
        //                     });
        //                 }

        //             }, 'json').done(function() {
        //                 console.log('Request done!');
        //             }).fail(function(jqxhr, settings, ex) {
        //                 console.log('failed, ' + ex);
        //                 Swal.fire({
        //                     text: "Something went wrong.",
        //                     icon: "error",
        //                     buttonsStyling: false,
        //                     confirmButtonText: "Ok, got it!",
        //                     customClass: {
        //                         confirmButton: "btn fw-bold btn-primary",
        //                     }
        //                 });
        //             });

        //         } else if (result.dismiss === 'cancel') {
        //             Swal.fire({
        //                 text: "Selected category was not deleted.",
        //                 icon: "error",
        //                 buttonsStyling: false,
        //                 confirmButtonText: "Ok, got it!",
        //                 customClass: {
        //                     confirmButton: "btn fw-bold btn-primary",
        //                 }
        //             });
        //         }
        //     });
        // });
    }

    // Toggle toolbars
    var toggleToolbars = function() {
        // Define variables
        const container = document.querySelector('#roles-datatable');
        const toolbarBase = document.querySelector('[data-table-toolbar="base"]');
        const toolbarSelected = document.querySelector('[data-roles-table-toolbar="selected"]');
        const selectedCount = document.querySelector('[ data-roles-table-select="selected_count"]');

        // Select refreshed checkbox DOM elements
        const allCheckboxes = container.querySelectorAll('tbody [type="checkbox"]');

        // Detect checkboxes state & count
        let checkedState = false;
        let count = 0;

        // Count checked boxes
        allCheckboxes.forEach(c => {
            if (c.checked) {
                checkedState = true;
                count++;
            }
        });

        
    }

    

    // end datatable and deleteation section




   






    // var handleBannerImageCRUDOperations = () => {

    //     let BannerImageDropzone = new Dropzone("#banner_images_dropzone", {
    //         url: `${api_config.upload_banner_images}`,
    //         acceptedFiles: ".jpeg,.jpg,.png",
    //         maxFiles: 10,
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
    //                 formData.append("csrfmiddlewaretoken", `${api_config.csrfmiddlewaretoken}`);
    //             });
    //             this.on("success", function(file, responseText) {
    //                 if(responseText.status_code == 200)
    //                 {
    //                     dt.draw();
    //                     let childElements = file?.previewElement?.children;
    //                     childElements.forEach(childElement => {
    //                         childElement.setAttribute('instance_id', responseText.data);
    //                     });
    //                 }
    //             });
    //             this.on('removedfile', function(file) {
    //                 let removeElement = file.previewElement.getElementsByTagName('a')?.[0];
    //                 let instance_id = removeElement.getAttribute('instance_id')
    //                 console.log(file)
    //                 // $.post(`${api_config.delete_records}`, { ids: [instance_id] }, 
    //                 //     function(data, status, xhr) {
    //                 //         if(data.status_code == 200)
    //                 //         {
    //                 //             dt.draw();
    //                 //         }

    //                 // }).done(function() { console.log('Request done!'); })
    //                 // .fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });

    //             }); 
    //         }
    //     });



        
    // }







    





    


    


    // end banner images crud operation





    



    // Public methods
    return {
        init: function() {
            initDatatable();
            handleSearchDatatable();
            initToggleToolbar();
            handleDeleteRows();





        }
    }

}();

// On document ready
KTUtil.onDOMContentLoaded(function() {
    DatatablesAndCRUDOperationServerSide.init();
});



function keyispressed(evt){
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    console.log(ASCIICode)
    if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57) && (ASCIICode < 97 || ASCIICode > 105) &&  ASCIICode != 116)
        return false;
    return true;
}
