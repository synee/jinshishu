app = angular.module("writer", ['ngRoute', 'ngCookies', 'ngExtends', 'textAngular',
                                'drahak.hotkeys', 'ui.bootstrap', 'jinshishu.service'])

.run ($http, $cookies)->
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken']

.directive 'ngRightClick', ($parse) ->
    return (scope, element, attrs, event) ->
        fn = $parse(attrs.ngRightClick)
        element.bind('contextmenu', (event) ->
            scope.$apply(() ->
                event.preventDefault();
                fn(scope, {$event: event})
            )
        )

.controller "DashboardController", ($scope, $modal, ArticleService, $log, $interval)->
    $scope.books = []
    $scope.refresh = ->
        ArticleService.getBooks().success((resp)-> $scope.books = resp)

    openBookForm = (book, callback)->
        bookCreateModal = $modal.open({
            templateUrl: "/static/application/templates/books/book_create.html"
            controller: "BookCreateController"
            windowClass: "book_form"
            resolve:
                book: ->
                    book
        })
        bookCreateModal.result.then(callback, -> $log.info('Modal dismissed at: ' + new Date()));

    $scope.bookContextMenu = (book)->
        openBookForm(book, (updatedBook) ->
            ArticleService.updateBook(updatedBook).success((resp)->
                book = resp
                book.active = true
            )
        )

    $scope.addBook = ()->
        openBookForm {}, (book) ->
            ArticleService.createBook(book).success (resp)->
                if resp.errors then return $log.error(resp.errors)
                $scope.books.push(resp)
                resp.active = true

    $scope.selectBook = (book)->
        $scope.currentBook = book
        if not book.articles
            ArticleService.getArticles(book.id).success((articles)-> book.articles = articles)

    $scope.selectArticle = (article)->
        $scope.currentArticle = article
        if article.content == undefined
            ArticleService.getArticle(article.id).success((resp)-> article.content = resp.content)
        $scope.showMenu = false

    $scope.addArticle = ()->
        ArticleService.createArticle($scope.currentBook.id).success (article)->
            if article.errors then return $log.error(article.errors)
            if not $scope.currentBook.articles then $scope.currentBook.articles = []
            $scope.currentBook.articles.push(article)
            article.active = true

    $scope.updateArticle = (article = $scope.currentArticle)->
        if not article.hasChanged then return
        ArticleService.updateArticle(article).success (resp)->
            if article.errors then return $log.error(article.errors)
            article.hasChanged = false

    $scope.onDelete = ($data, $event)->
        obj = $data[1]
        switch $data[0]
            when 'book'
                if not $promise = ArticleService.deleteBook(obj)
                    return
                objs = $scope.books
            when 'article'
                if not $promise = ArticleService.deleteArticle(obj)
                    return
                objs = $scope.currentBook.articles
            else return
        index = objs.indexOf(obj)
        if index < 0 then return
        $promise.success((resp)-> if resp.success then objs.splice(index, 1))

    $interval (-> $scope.updateArticle()), 60 * 1000

    $scope.refresh()

.controller "BookCreateController", ($scope, $modalInstance, book)->
    $scope.book = book
    $scope.ok = () ->
        $modalInstance.close($scope.book)

    $scope.cancel = () ->
        $modalInstance.dismiss('cancel');
