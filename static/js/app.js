var app = angular.module('debugToolApp', ['ui.router', 'ngMaterial']);

app.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider)
{
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/debug");
  // Now set up the states
  $stateProvider
    .state('debug', {
      url: "/debug",
      templateUrl: "/static/ng-templates/debug.html",
      controller: "DebugCtrl"
    });
}]);
