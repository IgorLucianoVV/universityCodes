(defproject blockchain "0.1.0-SNAPSHOT"
  :description "Blockchain simples usando Clojure e Compojure"
  :dependencies [[org.clojure/clojure "1.10.3"]
                 [compojure "1.6.2"]
                 [ring/ring-defaults "0.3.3"]
                 [cheshire "5.10.0"]]
  :main ^:skip-aot blockchain.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
