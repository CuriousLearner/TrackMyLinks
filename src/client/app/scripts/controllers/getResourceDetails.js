app.controller('getResourceDetails',function($scope, $http) {
  $scope.resources = [];
  $scope.reverseSort = false;
  $scope.is_data = false;
  $scope.getData = function() {
    $scope.resources = [];
    $http({
      method: 'GET', 
      url: 'http://localhost:5000/api/resource/getresources/', 
      headers: {'Access-Control-Allow-Origin': '*'}
    }).success(function(data){
      $scope.resources = data;
      if($scope.resources.length) {
        $scope.is_data = true;
      }
    }).
    error(function(data){
      console.log("Unable to fetch resources");
      $scope.is_data = false;
    });
  }
});