$(document).ready(function () {

    var start_point_err;
    var end_point_err;
    var date_err;

    $('.start_txt').keyup(function () {
        start_point_chek();

    });

    function start_point_chek() {
        var start_point = $('.start_txt').val();
        console.log("***");

        if (start_point == '') {
            $('#startpoint').html("<b>Enter the Starting Point</b>");
            $('#startpoint').css("color", "red");
            start_point_err = false;
            return start_point_err;

        }
        else if (start_point != 'bhavnagar' && start_point != 'Bhavnagar' && start_point != 'ahmedabad' && start_point != 'Ahmedabad' && start_point != 'BHAVNAGAR' && start_point != 'AHMEDABAD') {
            $('#startpoint').html("<b>This city are not able</b>");
            $('#startpoint').css("color", "red");
            start_point_err = false;
            return start_point_err;

        }

        else {
            $('#startpoint').html("<b>&#10004;</b>");
            $('#startpoint').css("color", "green");
            start_point_err = true;
            return true;
        }



    }

    $('.end_txt').keyup(function () {
        end_point_chek();

    });

    function end_point_chek() {
        var end_point = $('.end_txt').val();
        // console.log("***");

        if (end_point == '') {
            $('#endpoint').html("<b>Enter the End Point</b>");
            $('#endpoint').css("color", "red");
            end_point_err = false;
            return end_point_err;

        }
        else if (end_point != 'bhavnagar' && end_point != 'Bhavnagar' && end_point != 'ahmedabad' && end_point != 'Ahmedabad' && end_point != 'BHAVNAGAR' && end_point != 'AHMEDABAD') {
            $('#endpoint').html("<b>This city are not able</b>");
            $('#endpoint').css("color", "red");
            end_point_err = false;
            return end_point_err;

        }

        else {
            $('#endpoint').html("<b>&#10004;</b>");
            $('#endpoint').css("color", "green");
            end_point_err = true;
            return true;
        }



    }
    $('.date_txt').keyup(function () {
        date_chek();

    });
    function date_chek() {
        var date = $('.date_txt').val();

        if (date == '') {
            $('#date').html("<b>Enter the Date</b>");
            $('#date').css("color", "red");
            date_err = false;
            return false;

        }
        else {
            $('#date').html("<b>&#10004;</b>");
            $('#date').css("color", "green");
            date_err = true;
            return true;
        }

    }
    $('#search').click(function () {
        var start = start_point_chek();
        var end = end_point_chek();
        var date = date_chek();
        if (start == true && end == true && date == true) {
            startpoint = $('.start_txt').val();
            endpoint = $('.end_txt').val();
            date = $('.date_txt').val();
            mydata = { start1: startpoint, end1: endpoint, date1: date }
            $.ajax({
                url: "/busselect/",
                type: "POST",
                data: mydata,
                success: function (data) {
                    console.log(mydata)
                },

            });
            return true;
        }
        else{
            return false;
        }



    });
});