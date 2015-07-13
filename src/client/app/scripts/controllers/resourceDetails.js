app.controller('resourceDetails', function($scope, $http, $routeParams, $location) {
  window.x = $scope;
  $scope.resourceId = $routeParams.resourceid;
  $scope.message = '';
  $scope.resource = {};
  // AJAX call to fetch the given resource
  $http({
    method: 'GET', 
    url: 'http://localhost:5000/api/resource/getresources/?resource_id=' + $scope.resourceId, 
    headers: {'Access-Control-Allow-Origin': '*'}
  }).
  success(function(data) {
    $scope.resource = data;
  }).
  error(function(data) {
    console.log("Unable to get Resource");
  });

  $scope.updateViewDetails = function() {
        $(document).ready( function() {
          $('#AlertMessage').delay(1000).fadeOut();
          $('#ModifyResourceForm').delay(2000).fadeOut();
          setTimeout(function () {
              $location.path('/').replace();
              $scope.$apply();
              }, 2500);
        });
        $scope.getData();
  }

  $scope.modify = function() {
    $http({
      method: 'PUT', 
      url: 'http://localhost:5000/api/resource/updateresources/' + $scope.resourceId + '/', 
      data: $scope.resource,
      headers: {
        'Content-Type':'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': ["POST, GET, OPTIONS, DELETE, PUT"]
      }
    }).
    success(function(data) {
      $scope.message = data[0].Message;
      $scope.updateViewDetails();
    }).
    error(function(data) {
      console.log("Unable to Modify Resource");
    });
  }

  $scope.delete = function() {
    $http({
      method: 'DELETE', 
      url: 'http://localhost:5000/api/resource/updateresources/' + $scope.resourceId + '/', 
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type':'application/json'
      }
    }).
    success(function(data) {
      $scope.message = data[0].Message;
      $scope.updateViewDetails();
    }).
    error(function(data) {
      console.log("Unable to Delete Resource");
    });
  }
});