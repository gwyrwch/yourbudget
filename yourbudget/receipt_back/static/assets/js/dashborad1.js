/*
 Template Name: Inspire - Bootstrap 4 Admin Dashboard
 Author: UIdeck
 Website: www.uideck.com
File: dashborad1 js
 */

!function ($) {
    "use strict";

    var Dashboard = function () {
    };
        //creates Bar chart
        Dashboard.prototype.createBarChart = function (element, data, xkey, ykeys, labels, lineColors) {
            Morris.Bar({
                element: element,
                data: data,
                xkey: xkey,
                ykeys: ykeys,
                labels: labels,
                gridLineColor: '#eee',
                barSizeRatio: 0.4,
                resize: true,
                hideHover: 'auto',
                barColors: lineColors
            });
        },

        //creates Donut chart
        Dashboard.prototype.createDonutChart = function (element, data, colors) {
            Morris.Donut({
                element: element,
                data: data,
                resize: true,
                colors: colors,
            });
        },

        Dashboard.prototype.init = function () {
            var th = this;

            var create_chart_1 = function(callback) {
                $.get('current_data?chart=overview', function(data) {
//              fixme: don't know why this works
//                    var $barData = [];
//
//                    var len = data.length;
//                    for (var i = 0; i < len; i++) {
//                        $barData.push({
//                            y: data[i]['y'],
//                            a: data[i]['a'],
//                            b: data[i]['b'],
//                            c: data[i]['c']
//                        });
//                    }

                    if (callback)
                        callback(data['overview'], data['top3']);
                }, "json");
            };

            create_chart_1(function($data, $top3){
                th.createBarChart('morris-bar-example', $data, 'y', ['a', 'b', 'c'], $top3, ['#f78fb3','#f5cd79', '#74b9ff']);
            });

            var create_chart_2 = function(callback) {
                $.get('current_data?chart=categorization', function(data) {
                    if (callback)
                        callback(data);
                }, "json");
            };

            create_chart_2(function($data){
                th.createDonutChart('morris-donut-example', $data, ['#f78fb3', "#f5cd79", '#74b9ff', '#9fcd91']);
            });

            //creating donut chart for dashboard-1
//            var $donutData = [
//                {label: "Grocery", value: 62},
//                {label: "Clothes", value: 29},
//                {label: "Food", value: 5},
//                {label: "Electronics", value: 4},
//            ];

        },
        //init
        $.Dashboard = new Dashboard, $.Dashboard.Constructor = Dashboard
}(window.jQuery),

//initializing
    function ($) {
        "use strict";
        $.Dashboard.init();
    }(window.jQuery);