using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement; // Corrigir o erro no nome do namespace

public class menuPrincipalManager : MonoBehaviour
{
    [SerializeField] private string nomeDoLevelDeJogo;

    [SerializeField] private string Menu;
    [SerializeField] private GameObject painelMenuInicial;
    [SerializeField] private GameObject painelOpcoes;
    [SerializeField] private GameObject painelMapas;

    public void Jogar () 
    {
        SceneManager.LoadScene(nomeDoLevelDeJogo); // Usar a variável nomeDoLevelDeJogo
    }

     public void irParaMenu () 
    {
        SceneManager.LoadScene(Menu); // Usar a variável nomeDoLevelDeJogo
    }

       public void AbrirMapas()
    {
        painelMapas.SetActive(true);
        painelMenuInicial.SetActive(false);
        painelOpcoes.SetActive(false);
    }

    public void AbrirOpcoes()
    {
        painelMenuInicial.SetActive(false);
        painelOpcoes.SetActive(true);
        painelMapas.SetActive(false);
    }

    public void FecharOpcoes()
    {
        painelMapas.SetActive(false);
        painelMenuInicial.SetActive(true);
        painelOpcoes.SetActive(false);
    }

    public void SairJogo()
    {
        Debug.Log("Sair do Jogo");
        Application.Quit(); // Corrigir erro de digitação
    }
}
