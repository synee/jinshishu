angular.module("ngContextMenu", [])

.directive('ngContextMenu', ($parse)->
    link: (scope, element, attrs, event)->
        console.log($parse(attrs.ngContextMenu))
)