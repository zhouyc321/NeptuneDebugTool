var app = angular.module('debugToolApp');

app.controller('DebugCtrl', ['$scope', '$state', '$log', '$stateParams', '$http', function($scope, $state, $log, $stateParams, $http) {
    $scope.customStyle = {};
    $scope.turnGreen = function (){
        $scope.customStyle.style = {"color":"green"};
    }

    $scope.turnRed = function() {
        $scope.customStyle.style = {"color":"red"};
    }


    $scope.debug = function(adgroup_id) {
        $log.log('debug clicked');
        $http.get("/data/debug/" + adgroup_id).then(function (response) {
            if (response.data.doc_id == -1) {
                $scope.turnRed();
            }
            else {
                $scope.turnGreen();
            }
            $scope.adgroup_id = adgroup_id;
            $scope.debugStr = response.data;
        });
    }

    var tabs = [
          { title: 'One', content: "Tabs will become paginated if there isn't enough room for them."},
          { title: 'Selfsold', content: "Selfsold Debug Info"},
          { title: 'Three', content: "You can bind the selected tab via the selected attribute on the md-tabs element."},
          { title: 'Four', content: "If you set the selected tab binding to -1, it will leave no tab selected."},
          { title: 'Five', content: "If you remove a tab, it will try to select a new one."},
          { title: 'Six', content: "There's an ink bar that follows the selected tab, you can turn it off if you want."},
          { title: 'Seven', content: "If you set ng-disabled on a tab, it becomes unselectable. If the currently selected tab becomes disabled, it will try to select the next tab."},
          { title: 'Eight', content: "If you look at the source, you're using tabs to look at a demo for tabs. Recursion!"},
          { title: 'Nine', content: "If you set md-theme=\"green\" on the md-tabs element, you'll get green tabs."},
          { title: 'Ten', content: "If you're still reading this, you should just go check out the API docs for tabs!"}
        ],
        selected = null,
        previous = null;

    var selectedTabs = [
        ],
        selected = null,
        previous = null;

    $scope.selectedTabs = selectedTabs;
    $scope.tabs = tabs;
    $scope.selectedIndex = 2;
    $scope.$watch('selectedIndex', function(current, old){
      previous = selected;
      selected = selectedTabs[current];
    });
    $scope.addTab = function (title, view) {
      view = view || title + " Content View";
      selectedTabs.push({ title: title, content: view, disabled: false});
    };
    $scope.removeTab = function (tab) {
      var index = selectedTabs.indexOf(tab);
      selectedTabs.splice(index, 1);
    };

}])


