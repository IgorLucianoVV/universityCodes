(ns financeiro.blockchain
  (:require [cheshire.core :as json])
  (:import (java.nio.charset Charset)
           (java.security MessageDigest)))

(defn sha256 [data]
  (let [message-digest (MessageDigest/getInstance "SHA-256")]
    (->> (.digest message-digest (.getBytes data (Charset/forName "UTF-8")))
         (map #(format "%02x" %))
         (apply str))))

(defn criar-bloco [indice nonce dados hash-anterior]
  (let [dados-str (json/generate-string dados)]
    {:indice indice
     :nonce nonce
     :dados dados-str
     :hash-anterior hash-anterior
     :hash (sha256 (str indice nonce dados-str hash-anterior))}))

(defn bloco-valido? [bloco]
  (= (subs (:hash bloco) 0 4) "0000"))

(defn encontrar-nonce [indice dados hash-anterior]
  (loop [nonce 0]
    (let [bloco (criar-bloco indice nonce dados hash-anterior)]
      (if (bloco-valido? bloco)
        nonce
        (recur (inc nonce))))))

(def bloco-genesis
  (let [dados "Bloco Gênesis"
        nonce (encontrar-nonce 0 dados "00000000000000000000000000000000")]
    (criar-bloco 0 nonce dados "00000000000000000000000000000000")))

(defonce blockchain (atom [bloco-genesis]))

(defn bloco-mais-recente []
  (last @blockchain))

(defn adicionar-bloco [dados]
  (let [bloco-anterior (bloco-mais-recente)
        indice (inc (:indice bloco-anterior))
        hash-anterior (:hash bloco-anterior)
        nonce (encontrar-nonce indice dados hash-anterior)
        novo-bloco (criar-bloco indice nonce dados hash-anterior)]
    (swap! blockchain conj novo-bloco)))

(defn obter-blockchain []
  @blockchain)
