// Funcion para cambiar el estatus de un cliente si es confiable o no
function cambiar_confiable(id) {
                $.ajax({
                    url: "/administrador/fotografo/cambiar_confiable/"+id,
                    data: {pk: id},
                    type: "POST", // http method
                    // handle a successful response
                    success: function (aData) {
                        $('#tabla').dataTable()._fnAjaxUpdate();
                    },

                    // handle a non-successful response
                    error: function (xhr, errmsg, err) {
                        alert("Ocurrio un error: " + xhr.responseJSON.Error);
                        $('#tabla').dataTable()._fnAjaxUpdate();
                    }
                });
            }