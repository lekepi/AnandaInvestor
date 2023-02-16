$(document).ready(function(){

    // loading spinner - about.html
    $("#ajax_sample").click(function(){
       var search = $('#search').val();
       $('.response').empty();
        $.ajax({
            url: '/fetchdata',
            type: 'post',
            data: {search:search},
            beforeSend: function(){
                //show spinner
                $("#loader").show();
            },
            success: function(response){
                $('.response').append(response.htmlresponse);
            },
            complete:function(data){
                //hide spinner
               $("#loader").hide();
            }
        });
    });

    // loading spinner - bt_stoploss.html
    $("#stop_loss").click(function(){
       var start_date = $('#sl_start_date').val();
       var end_date = $('#sl_end_date').val();
       var alpha_up = $('#sl_alpha_up').val();
       var alpha_down = $('#sl_alpha_down').val();
       $('#sl_response').empty();
        $.ajax({
            url: '/stoploss_getdata',
            type: 'post',
            data: {start_date:start_date, end_date:end_date,alpha_up:alpha_up, alpha_down:alpha_down},
            beforeSend: function(){
                //show spinner
                $("#sl_loader").show();
            },
            success: function(response){
                $("#sl_loader").hide();
                $('#sl_response').append(response.htmlresponse);
                //$.fn.dataTableExt.sErrMode = 'throw';
                $('.datatable_bootstrap').DataTable().ajax.reload();
            },
            complete:function(data){
                //hide spinner
                $("#sl_loader").hide();
            }
        });
    });

    function formatNumber(num) {
        return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
    }


    $('.datatable_bootstrap').DataTable({
        "pageLength": 50,
    });

    $('.datatable_bootstrapInv').DataTable({
        "pageLength": 25,
        "order": [[ 3, "asc" ]]
    });

    $('.datatable_bootstrapInvClose').DataTable({
        "pageLength": 25,
        "order": [[ 1, "asc" ]]
    });


    $('.datatable_bootstrap_col1_desc').DataTable({
        "pageLength": 50,
        "order": [[ 0, "desc" ]]
    });

     $('.datatable_bootstrap_col2_asc').DataTable({
        "pageLength": 50,
        "order": [[ 1, "asc" ]]
    });

    $('.datatable_bootstrap_col3_desc').DataTable({
        "pageLength": 50,
        "order": [[ 2, "desc" ]]
    });

     $('.datatable_bootstrap_col5_desc').DataTable({
        "pageLength": 50,
        "order": [[ 4, "desc" ]]
    });


    $('.wide_string_field').width("300px")


    // Navbar
    // hide one 'Analyst menu' if person is Analyst and AnalystAdmin
    if ($('#navbar_analyst1').is(":visible") && $('#navbar_analyst2').is(":visible"))
    {
        $('#navbar_analyst2').hide();
    }

    // top_page_title
    // top_page_title color change when Hover
    $(".top_page_title").hover(function(){
        $(this).css('color', 'blue');
    },
    function(){
        $(this).css('color', '#444444');
    });

    // toggle the menu from the top page title
     $('.top_page_title').click(function(){
         $('.full_left_menu').toggle();
         let top_page_title = $('.top_page_title').text();
            top_page_title = top_page_title.substring(2);
         if($('.full_left_menu').is(":visible")) {
             $(this).text('< '+top_page_title);
         } else {
             $(this).text('> '+top_page_title);
         }
    });


      // trade date picker: put end date=start date
      $("#dp_start_trades").change(function(){
          jsDate =$(this).val()
          $('#dp_end_trades').val(jsDate);
      });

      $("#alpha_stock_ticker").change(function(){
          $('#alpha_stock_group').val(0);
      });



      //Analyst - universe
      $(".tooltip_stock").hover(function(){
        $(this).css({'color':'blue'});
      },
      function(){
        $(this).css({'color':'#444444'});
      });

      // TEST on trading/Home
      $("#jquery_test").click(function(){
        $(this).hide();
      });

      $("#jquery_test").hover(function(){
        $(this).css("background-color", "yellow");
      },
      function(){
        $(this).css("background-color", "white");
      });

    // format dashboard table
    $("td.dashboard_val10:contains('-')").addClass('red');
    $("td.dashboard_val10:not(:contains('-'))").addClass('green');
    $("td.dashboard_val11:contains('-')").addClass('red');
    $("td.dashboard_val11:not(:contains('-'))").addClass('green');
    $("td.dashboard_val12:contains('-')").addClass('red');
    $("td.dashboard_val12:not(:contains('-'))").addClass('green');

    $('td.dashboard_val2').each(function() {
    var val = parseInt($(this).text());
    val = formatNumber(val);
    $(this).text(val);
    })

    $('td.dashboard_val12').each(function() {
    var val = parseInt($(this).text());
    val = formatNumber(val);
    $(this).text(val);
    })

    //$('.td_date_format').each(function() {
    //var val = $(this).text();
    //val = val.substring(0, 10)
    //$(this).text(val);
   // })


});