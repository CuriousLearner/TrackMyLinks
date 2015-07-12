// Main Angular app module

var app = angular.module('ResourcesApp', ['ngRoute', 'ngTagsInput']);

app.config(['$routeProvider', function($routeProvider){
  $routeProvider.
    when('/resource/:resourceid', {
      templateUrl: '../views/resource-details.html',
      controller: 'resourceDetails'
    }).
    otherwise({
      redirectTo: '/'
    });
}]);