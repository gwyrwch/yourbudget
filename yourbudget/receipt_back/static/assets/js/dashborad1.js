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
                var all_colors = ['#f78fb3', "#f5cd79", '#74b9ff', '#9fcd91'];
                th.createDonutChart('morris-donut-example', $data, all_colors);
            });
        },
        //init
        $.Dashboard = new Dashboard, $.Dashboard.Constructor = Dashboard
}(window.jQuery),

//initializing
    function ($) {
        "use strict";
        $.Dashboard.init();
    }(window.jQuery);