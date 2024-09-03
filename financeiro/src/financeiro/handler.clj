(ns financeiro.handler
  (:require [cheshire.core :as json]
            [compojure.core :refer [defroutes GET POST]]
            [compojure.route :as route]
            [financeiro.db :as db]
            [financeiro.transacoes :as transacoes]
            [financeiro.blockchain :as blockchain]
            [ring.middleware.defaults :refer [api-defaults wrap-defaults]]
            [ring.middleware.resource :refer [wrap-resource]]
            [ring.middleware.content-type :refer [wrap-content-type]]
            [ring.middleware.json :refer [wrap-json-body]]
            [ring.util.response :refer [resource-response file-response content-type]]))

(defn como-json [conteudo & [status]]
  {:status (or status 200)
   :headers {"Content-Type" "application/json; charset=utf-8"}
   :body (json/generate-string conteudo)})

(defroutes app-routes
  (GET "/" [] (-> (file-response "./resources/public/index.html") (content-type "text/html")))

  (GET "/saldo" [] (como-json {:saldo (db/saldo)}))

  (POST "/transacoes" requisicao
    (if (transacoes/valida? (:body requisicao))
      (-> (db/registrar (:body requisicao))
          (como-json 201))
      (como-json {:mensagem "Requisição inválida"} 422)))

  (GET "/transacoes" {filtros :params}
    (como-json {:transacoes (if (empty? filtros) (db/transacoes)
                                (db/transacoes-com-filtro filtros))}))

  (GET "/receitas" [] (como-json {:transacoes (db/transacoes-do-tipo "receita")}))

  (GET "/despesas" [] (como-json {:transacoes (db/transacoes-do-tipo "despesa")}))

  ;; Rotas para a blockchain
  (POST "/blockchain/transacao" requisicao
    (let [dados (:body requisicao)]
      (blockchain/adicionar-bloco dados)
      (como-json {:mensagem "Transação adicionada na blockchain com sucesso!"} 201)))

  (GET "/blockchain" []
    (como-json {:blockchain (blockchain/obter-blockchain)}))

  (route/not-found "Recurso não encontrado"))

(def app
  (-> (wrap-defaults app-routes api-defaults)
      (wrap-json-body {:keywords? true :bigdecimals? true})
      (wrap-resource "public")
      wrap-content-type))
