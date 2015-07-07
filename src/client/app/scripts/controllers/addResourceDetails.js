app.controller('addResourceDetails',function($scope, $http) {
  window.x = $scope;
  $scope.resource = {};
  $scope.message = {};
  $scope.submit = function() {
    $http({method: 'POST', 
      url: 'http://localhost:5000/api/resource/addresources/', 
      data: $scope.resource, 
      headers: {'Access-Control-Allow-Origin': '*'}
      }).success(function(data){
        $scope.message = data.Success;
      }).
      error(function(data){
        console.log("Unable to fetch resources");
        $scope.message = data.Error;
      });
    };
});