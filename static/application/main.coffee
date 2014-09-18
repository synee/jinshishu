app = angular.module('jinshishu', ['ngRoute', 'ngCookies', 'ui.bootstrap', 'ngCommunity'])

.run(($http, $cookies)->
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
)
.config ($httpProvider) ->
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

.factory("paramsTraditional", [ ->
        buildParams = (prefix, obj, traditional, add) ->
            if (Array.isArray(obj))
                for v, i in obj
                    if traditional || /\[\]$/.test(prefix)
                        add(prefix, v)
                    else
                        buildParams("#{prefix}[#{if typeof v == "object" then i else ""}]", v, traditional, add);
            else if !traditional && typeof obj == "object"
                for name, value in obj
                    buildParams("#{prefix}[#{name}]", value, traditional, add)
            else
                add(prefix, obj)

        return (a, traditional = true)->
            prefix
            s = []
            add = (key, value) ->
                value = if (typeof value == "function") then value() else (if value == null then "" else value)
                s[s.length] = "#{encodeURIComponent(key)}=#{encodeURIComponent(value)}"

            if Array.isArray(a)
                for item in a
                    add(item.name, item.value);
            else
                for prefix, value of a
                    buildParams(prefix, value, traditional, add)
            return s.join("&").replace(/%20/g, "+")
    ])

.directive('input', ['$parse', ($parse) ->
        restrict: 'E',
        require: '?ngModel',
        link: (scope, element, attrs) ->
            if(attrs.value && $parse(attrs.ngModel).assign)
                $parse(attrs.ngModel).assign(scope, attrs.value);
    ])
.directive('textarea', ['$parse', ($parse) ->
        restrict: 'E',
        require: '?ngModel',
        link: (scope, element, attrs) ->
            if not scope.form
                return
            scope.form[attrs.name] = element.val()
            if(attrs.value && $parse(attrs.ngModel).assign)
                $parse(attrs.ngModel).assign(scope, attrs.value);
    ])

.directive('option', ['$parse', ($parse) ->
        restrict: 'E',
        require: '?ngModel',
        link: (scope, element, attrs) ->
            if(attrs.selected)
                element[0].selected = true
    ])


.directive('form', ['$parse', '$http', 'paramsTraditional', ($parse, $http, paramsTraditional) ->
        restrict: 'E',
        require: '?ngModel',
        link: (scope, element, attrs) ->
            scope.submit = ->
                $http
                    method: "post",
                    url: attrs.actionUrl,
                    data: paramsTraditional(@form)
                    headers:
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                .success((resp)->
                    console.log(resp)
                )

    ])
