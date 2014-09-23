angular.module("ngExtends", [])

.value('$dragData', {$event: null, $data: null})

.directive("ngDrag", ($parse, $dragData)->
    link: (scope, element, attrs)->
        angular.forEach(element, (el)->
            el.draggable = true
        )
        element.on("dragstart", (event)->
            $dragData.$event = event
            $dragData.$data = $parse(attrs.ngDrag)(scope)
        )
)


.directive("ngDrop", ($parse, $dragData)->
    link: (scope, element, attrs)->
        element.on("dragover", (e)->
            e.preventDefault()
        )
        element.on("drop", (event)->
            $dragData.$event = event
            $dragData.$event.$data = $dragData.$data
            $parse(attrs.ngDrop)(scope, $dragData)
        )
)

.directive("ngScroll", ($parse, $document, $window, $log)->
    link: (scope, element, attrs)->
        $document.on("scroll", (event)->
            scope.$apply(->
                $parse(attrs.ngScroll)(scope, {
                    $event: event
                    $scrollX: $window.scrollX
                    $scrollY: $window.scrollY
                })
            )
        )
)