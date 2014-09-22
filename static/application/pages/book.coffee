angular.module('book', ['jinshishu.service', 'jinshishu.public', 'ui.bootstrap'])

.controller('BookController', ($scope)->
    $scope.book = window.session.book
)