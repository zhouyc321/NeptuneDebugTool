var app = angular.module('debugToolApp');

app.controller('DebugCtrl', ['$scope', '$state', '$log', '$stateParams', '$http', function($scope, $state, $log, $stateParams, $http) {
    $scope.customStyle = {};
    selfsoldTurnGreen = function (){
        $scope.customStyle.selfsoldToolbar = {"background-color":"#72d572"};
    }

    selfsoldTurnRed = function() {
        $scope.customStyle.selfsoldToolbar = {"background-color":"#f2525d"};
    }

    budgetTurnGreen = function (){
        $scope.customStyle.budgetToolbar = {"background-color":"#72d572"};
    }

    budgetTurnRed = function() {
        $scope.customStyle.budgetToolbar = {"background-color":"#f2525d"};
    }

    $scope.debug = function(adgroup_id) {
        $log.log('debug clicked');
        var length = selectedModules.length;
        for (var i = 0; i < length; i++) {
            if (selectedModules[i] == "selfsold") {
                $http.get("/data/selfsold/" + adgroup_id).then(function (response) {
                    if (response.data.doc_id == -1) {
                        selfsoldTurnRed();
                        log = [];
                    }
                    else {
                        selfsoldTurnGreen();
                    }
                    $scope.adgroup_id = adgroup_id;
                    $scope.selfsold = response.data;
                });
            }
            if (selectedModules[i] == "budget") {
                $http.get("/data/budget/" + adgroup_id).then(function (response) {
                    if (response.data.doc_id == -1) {
                        budgetTurnRed();
                        log = [];
                    }
                    else {
                        budgetTurnGreen();
                    }
                    $scope.adgroup_id = adgroup_id;
                    $scope.budget = response.data;
                });
            }

        }
    }

    $scope.toggle = function (item, list) {
        var idx = list.indexOf(item);
        if (idx > -1) {
          list.splice(idx, 1);
        }
        else {
          list.push(item);
        }
    };
    var selectedModules = [];
    $scope.selectedModules = selectedModules;
    var tabs = [
          { title: 'One', content: "Tabs will become paginated if there isn't enough room for them."},
          { title: 'Selfsold', content: "Selfsold Debug Info"},
          { title: 'Three', content: "You can bind the selected tab via the selected attribute on the md-tabs element."},
         ],
        selected = null,
        previous = null;
    $scope.tabs = tabs;
}])
