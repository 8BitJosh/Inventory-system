$(document).ready(function() {

    fillList('');

    $('#items_table').on('click', '#item', function(){
        var index = $(this).closest('tr').index();
        var val = $('table#items_table tr:eq(' + index + ') td:eq(' + 0 + ')').text();
        console.log(val);
        fillPopup(val);
        $('#popup').modal('show');
    });


    $('#Search').on('input', function(e){
        var query = $('#Search').val();
        fillList(query);
    });


    $('#new').on('click', function(e){
        getNewID();
    });


    $('#popup').on('hidden.bs.modal', function(e){
        clearPopup();
    });


    $('#update').on('click', function(){
        var vals = {};
        $('#itemForm').serializeArray().map(function(x){vals[x.name] = x.value;});
        vals.id = $('#id').val();

        $.ajax({url: '/api/single/' + $('#id').val(),
            type: 'POST',
            data: vals,
            dataType: 'json',
            success: function(data){
                refresh();
            }
        });
    })


    $('#delete').on('click', function(e){
        $.ajax({url: '/api/single/' + $('#id').val(),
            type: 'DELETE',
            success: function(data){
                refresh()
            }
        });
    });

});


function clearList(){
    $('#items_table tr:gt(0)').remove();
}


function fillList(query){
    $.ajax({url: '/api/search',
        type: 'GET',
        data: {'query': String(query)},
        dataType: 'json',
        success: function(data){
            clearList();

            $.each(data.data, function(index, item){
                $('<tr id="item">').html("<td>" + item.id + "</td><td>" + 
                    item.name + "</td>").appendTo('#items_table');
            })
        }
    });
}


function clearPopup(){
    console.log("close");
    
    $('#id').val('');
    $('#name').val('');
    $('#store').val('');
    $('#location').val('');
    $('#other').val('');
}


function refresh(){
    $('#popup').modal('hide');
    fillList($('#Search').val());
}


function fillPopup(id){
    $.ajax({url: '/api/single/' + String(id),
        type: 'GET',
        dataType: 'json',
        success: function(data){
            $('#id').val(data.id);
            $('#name').val(data.name);
            $('#store').val(data.store);
            $('#location').val(data.location);
            $('#other').val(data.other);
        }
    });
    
    console.log("fillpop = " + String(id));
}


function getNewID(){

    $.ajax({url: '/api/ID',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            console.log(data);
            $('#id').val(data.id);
        }
    });
}