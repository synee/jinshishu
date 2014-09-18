angular.module("ngCommunity", [])

.factory("commentService", ($http, paramsTraditional)->
    loadComments: (contentType, contentPk, offset = 0, size = 10)->
        $http.get("/comments/#{contentType}/#{contentPk}/#{offset}-#{size}")
    postComment: (contentType, contentPk, comment) ->
        $http.post("/comments/#{contentType}/#{contentPk}", paramsTraditional({
            comment: comment
        }))
)
.directive("comments", (commentService)->
    templateUrl: "/static/application/templates/community/comments.html"
    restrict: 'E',
    require: '?ngModel',
    scope:
        contentType: "@"
        contentPk: "@"
    replace: true
    transclude: true,
    link: (scope, element, attrs)->
        commentService.loadComments(
            scope.contentType,
            scope.contentPk,
        ).success((resp)->
            scope.comments = resp
        )
        scope.submit = ->
            commentService.postComment(scope.contentType, scope.contentPk, scope.newComment)
            .success((resp)->
                scope.newComment = ''
                scope.comments.push(resp)
            )
)

.directive("tagbar", ($http)->
    restrict: 'E',
    require: '?ngModel',
    link: (scope)->
        scope.addTag = (newTag)->
            console.log(newTag)
        scope.addBlur = ()->
            scope.shownew = false
)
