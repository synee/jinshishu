app = angular.module("search", ['ngRoute', 'ngExtends', 'ui.bootstrap', 'jinshishu.service', 'jinshishu.public'])

.controller("SearchController", ($scope, $timeout, ArticleService, SearchService)->
    $scope.keywords = ''
    $scope.searchedWords = []
    $scope.onScroll = ($scrollY)->
        if $scrollY > 64
            $scope.navClass = "fixed"
        else
            $scope.navClass = ""


    $scope.selectTab = (tab) ->
        $scope.currentTab = tab

    $scope.search = ()->
        if $scope.searching then return
        $scope.searching = true
        $timeout(->
            keywords = $scope.keywords
            tab = $scope.currentTab
            SearchService.search(tab, keywords).success((resp)->
                $scope["#{tab}List"] = resp
                $scope.searchedWords.push({
                    tab: tab
                    keywords: keywords
                    results: resp
                })
            ).finally(->
                $scope.searching = false
            )
        , 500)
)

.controller('BookItemController', ($scope) ->
    console.log($scope.book.date_updated, ":", $scope.book.date_created)
)