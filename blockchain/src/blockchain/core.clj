(ns blockchain.core
  (:require [compojure.core :refer [defroutes GET POST]]
            [compojure.route :as route]
            [ring.adapter.jetty :as jetty]
            [ring.middleware.defaults :refer [wrap-defaults site-defaults]]
            [cheshire.core :as json]
            [clojure.java.io :as io])
  (:gen-class))

(defonce blockchain (atom []))

(defn calculate-hash [block]
  (let [block-data (str (:index block)
                        (:timestamp block)
                        (:transactions block)
                        (:previous-hash block))]
    (-> block-data
        (.getBytes "UTF-8")
        (java.security.MessageDigest/getInstance "SHA-256")
        (.digest)
        (java.util.Base64/getEncoder)
        (.encodeToString))))

(defn create-block [transactions previous-hash]
  (let [index (count @blockchain)
        timestamp (System/currentTimeMillis)
        block {:index index
               :timestamp timestamp
               :transactions transactions
               :previous-hash previous-hash
               :hash ""}]
    (assoc block :hash (calculate-hash block))))

(defn add-block [transactions]
  (let [previous-hash (if (empty? @blockchain) "0" (:hash (last @blockchain)))
        block (create-block transactions previous-hash)]
    (swap! blockchain conj block)
    block))

(defn get-blockchain []
  @blockchain)

(defn add-transaction [transaction]
  (add-block [transaction]))

(defroutes app-routes
  (GET "/" [] "Blockchain Server")
  (GET "/blockchain" [] {:status 200 :body (json/generate-string (get-blockchain))})
  (POST "/transaction" req
    (let [transaction (json/parse-string (slurp (:body req)) true)]
      (add-transaction transaction)
      {:status 200 :body (json/generate-string transaction)}))
  (route/not-found "Not Found"))

(def app
  (wrap-defaults app-routes site-defaults))

(defn -main [& args]
  (jetty/run-jetty app {:port 3000 :join? false}))
