app.controller('addResourceDetails',function($scope, $http) {
  window.x = $scope;
  $scope.resource = {};
  $scope.submit = function() {
    $http({method: 'POST', 
      url: 'http://localhost:5000/api/resource/addresources/', 
      data: $scope.resource, 
      headers: {'Access-Control-Allow-Origin': '*'}
      }).success(function(data){
        $scope.message = data.Message;
        $scope.getData();
      }).
      error(function(data){
        console.log("Unable to fetch resources");
        $scope.message = data.Error;
      });
    };
  $scope.reset = function() {
    $scope.resource = {};
  }
});