app = angular.module("search", [])

app.controller("searchBoxCtrl", ($scope)->
    $scope.search = (words, $event)->
        if ($event.keyCode == 13 && words)
            console.log(words)
)