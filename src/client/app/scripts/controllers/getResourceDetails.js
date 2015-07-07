app.controller('getResourceDetails',function($scope, $http) {
  $scope.resources = [];
  $scope.reverseSort = false;
  $http({method: 'GET', url: 'http://localhost:5000/api/resource/getresources/', headers: {
    'Access-Control-Allow-Origin': '*'}
  }).success(function(data){
    $scope.resources = data;
  }).
  error(function(data){
    console.log("Unable to fetch resources");
  });
});