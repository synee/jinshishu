angular.module("jinshishu.service", [])

.factory("SearchService", ($http)->
    search          : (type, q, page=0) ->
                                    $http.get("/api/search_#{type}", {params: {q: q, page_index: page, page_size: 20}})
)

.factory("ArticleService", ($http)->
    createBook      : (book)        -> $http.post("/p/api/book_create", book)
    updateBook      : (updatedBook) -> $http.post("/p/api/book_update", updatedBook)
    deleteBook      : (book)        -> if confirm("真的要删除 “#{book.name}” 吗?") then $http.post("/p/api/book_delete", book)
    getBooks        : ()            -> $http.get("/p/api/book_get")

    createArticle   : (bookId)      -> $http.post("/p/api/article_create", {book: bookId})
    updateArticle   : (article)     -> $http.post("/p/api/article_update", article)
    deleteArticle   : (article)     -> if confirm("真的要删除 “#{article.title}” 吗?") then $http.post("/p/api/article_delete", article)
    getArticles     : (bookId)      -> $http.get("/p/api/article_get", {params: book: bookId })
    getArticle      : (id)          -> $http.get("/p/api/article", {params: pk: id})
)
