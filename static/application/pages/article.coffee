angular.module('article', ['jinshishu.service', 'jinshishu.public', 'ui.bootstrap'])

.controller('ArticleController', ($scope)->
    $scope.article = window.session.article
)