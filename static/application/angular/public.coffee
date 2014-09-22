angular.module("jinshishu.public", [])

.controller("NavController", ($scope)->
    $scope.user = window.session.user
)